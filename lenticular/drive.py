import pickle
import os
import io
import yaml
from rich import print
from pathlib import Path
from tqdm import tqdm
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# From https://www.thepythoncode.com/article/using-google-drive--api-in-python
# Which is based on: https://developers.google.com/drive/api/quickstart/python
# Helful: https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/drive_v2.files.html

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


# read policies
def read_policies():
    with open("./lenticular/policies.yaml", "r") as file:
        policies = yaml.safe_load(file)
    return policies


def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if not os.path.exists("./lenticular/credentials.json"):
        print(
            "🚩 [bold red]No credentials.json file found.[/bold red]\n Please follow the instructions here:https://developers.google.com/drive/api/quickstart/python"
        )
        return None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./lenticular/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build("drive", "v3", credentials=creds)


def traverse_drive_folder(service, folder_id):
    """
    Recursively traverses a Google Drive folder tree and yields each file's content and path.

    Args:
        service: A Google Drive API service object authenticated with valid credentials.
        folder_id (str): The ID of the Google Drive folder to start the traversal from.

    Yields:
        Tuple[str, bytes]: A tuple containing the path and content of each file found in the folder structure.
    """
    try:
        # Retrieve all files and subfolders from the given folder
        results = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents",
                fields="nextPageToken, files(id, name, mimeType)",
            )
            .execute()
        )
        items = results.get("files", [])

        # Iterate over each file/folder in the current folder
        for item in items:
            if item["mimeType"] == "application/vnd.google-apps.folder":
                # Recursively traverse any subfolders
                yield from traverse_drive_folder(service, item["id"])
            else:
                # Fetch the file's content and yield its path and content
                request = service.files().get_media(fileId=item["id"])
                content = request.execute()

                path_parts = [item["name"]]
                parent_id = item["parents"][0]
                while parent_id != folder_id:
                    parent = (
                        service.files()
                        .get(fileId=parent_id, fields="id, name, parents")
                        .execute()
                    )
                    path_parts.insert(0, parent["name"])
                    parent_id = parent["parents"][0]
                path = "/".join(path_parts)

                yield path, content
    except HttpError as error:
        print(f"An error occurred: {error}")


class Drive:
    """
    Instantiate a Drive session.

    """

    def __init__(self):
        self.service = get_gdrive_service()
        self.policies = read_policies()

    def drive_request(self, q: str, recursive=False) -> list:
        """Send an API request to drive
        query syntax https://developers.google.com/drive/api/guides/search-files#examples

        """
        try:
            files = []
            page_token = None
            while True:
                # pylint: disable=maybe-no-member
                response = (
                    self.service.files()
                    .list(
                        q=q,
                        spaces="drive",
                        fields="nextPageToken, "
                        "files(id, name, mimeType, size, parents, modifiedTime)",
                        pageToken=page_token,
                    )
                    .execute()
                )

                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break

        except HttpError as error:
            print(f"An error occurred: {error}")
            files = None

        if recursive:
            for file in files:
                if file["mimeType"] == "application/vnd.google-apps.folder":
                    files.extend(self.folder_contents(file["id"]))
                    # TODO not actually recursive, only one level deep
                    # Better to get all folders and then iterate through them
                    # drop file from files
                    files.remove(file)
        return files

    def folder_contents(self, folder_id):
        """Return all files in a folder and its subfolders"""
        return self.drive_request(f"'{folder_id}' in parents", recursive=False)

    def list_folders(self):
        """List all folders in drive"""
        return self.drive_request("mimeType = 'application/vnd.google-apps.folder'")

    def search(self, query: str) -> list:
        """Search using the query syntax https://developers.google.com/drive/api/guides/search-files#examples"""
        return self.drive_request(f"{query}")

    def search_folders(self, folder_name: str) -> list:
        """Search for a folder by name"""
        return self.drive_request(
            f"name contains '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        )

    def search_files(self, query: str) -> list:
        """Search for a file by name"""
        return self.drive_request(
            f"name contains '{query}' and mimeType != 'application/vnd.google-apps.folder'"
        )

    def get_file_by_id(self, file_id: str) -> list:
        """Search for a file by ID"""
        return (
            self.service.files()
            .get(
                fileId=file_id, fields="id,name,mimeType,size,modifiedTime,md5Checksum"
            )
            .execute()
        )

    def download_file(self, file_id: str, path: str = None, name: str = None) -> dict:
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : dict with name, content and suffix | None
        ex: Path(f["name"]).with_suffix(f["suffix"]).write_bytes(f["content"])
        #TODO make async
        """
        file_data = self.get_file_by_id(file_id)
        kind = file_data.get("kind")
        mimeType = file_data.get("mimeType")
        if not name:
            name = file_data.get("name")

        # Google Docs, Sheets, Presentations and such must be converted first to a non-Google format
        if mimeType == "application/vnd.google-apps.document":
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            suffix = ".docx"
        elif mimeType == "application/vnd.google-apps.spreadsheet":
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            suffix = ".xlsx"
        elif mimeType == "application/vnd.google-apps.presentation":
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
            suffix = ".pptx"
        elif mimeType == "application/vnd.google-apps.drawing":
            request = self.service.files().export_media(
                fileId=file_id, mimeType="image/png"
            )
            suffix = ".png"
        elif mimeType == "application/vnd.google-apps.form":
            request = self.service.files().export_media(
                fileId=file_id, mimeType="application/pdf"
            )
            suffix = ".pdf"
        else:
            request = self.service.files().get_media(fileId=file_id)
            suffix = Path(name).suffix
        try:
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            if path:
                if path[-1] != "/":
                    path = path + "/"
                Path(path + name).with_suffix(suffix).write_bytes(file.getvalue())
                return {"name": name, "content": file.getvalue(), "suffix": suffix}
            else:
                return {"name": name, "content": file.getvalue(), "suffix": suffix}

        except HttpError as error:
            print(f"An error occurred: {error}")

    def download_folder(
        self, folder_id: str, path: str = Path.cwd(), name: str = None
    ) -> bool:
        """Downloads a folder
        Args:
            folder_id: ID of the folder to download
        Returns : bool
        """
        # get folder name
        if not name:
            name = self.get_file_by_id(folder_id)["name"]

        # create output path
        if self.policies and self.policies["output_path"]:
            path = self.policies["output_path"]

        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        # create a new subdirectory using name
        path = path / name
        path.mkdir(parents=True, exist_ok=True)

        # get all files in all folders and subfolders
        contents = self.folder_contents(folder_id)
        files = [
            file
            for file in contents
            if file["mimeType"] != "application/vnd.google-apps.folder"
        ]
        for file in tqdm(files, total=len(files), desc="Downloading files"):
            self.download_file(file["id"], path=str(path))

        subfolders = [
            folder
            for folder in contents
            if folder["mimeType"] == "application/vnd.google-apps.folder"
        ]
        for subfolder in subfolders:
            subpath = path / subfolder["name"]
            subpath.mkdir(parents=True, exist_ok=True)
            subcontents = self.folder_contents(subfolder["id"])
            files = [
                file
                for file in subcontents
                if file["mimeType"] != "application/vnd.google-apps.folder"
            ]
            for file in files:
                self.download_file(file["id"], path=str(subpath))

        return name
