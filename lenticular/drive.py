import pickle
import os
import io
from rich import print
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# From https://www.thepythoncode.com/article/using-google-drive--api-in-python
# Which is based on: https://developers.google.com/drive/api/quickstart/python

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if not os.path.exists('credentials.json'):
        print("🚩 [bold red]No credentials.json file found.[/bold red]\n Please follow the instructions here:https://developers.google.com/drive/api/quickstart/python")
        return None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)


class Drive:
    """
    Instantiate a multiplication operation.
    Numbers will be multiplied by the given multiplier.
    
    :param multiplier: The multiplier.
    :type multiplier: int
    """
    
    def __init__(self):
        self.service = get_gdrive_service()
    
    def drive_request(self, q:str, recursive=False) -> list:
        """Send an API request to drive
        query syntax https://developers.google.com/drive/api/guides/search-files#examples

        """
        try:
            files = []
            page_token = None
            while True:
                # pylint: disable=maybe-no-member
                response = self.service.files().list(q=q,
                                                spaces='drive',
                                                fields='nextPageToken, '
                                                    'files(id, name, mimeType, size, parents, modifiedTime)',
                                                pageToken=page_token).execute()
                    
                files.extend(response.get('files', []))
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

        except HttpError as error:
            print(F'An error occurred: {error}')
            files = None
        
        if recursive:
            for file in files:
                if file["mimeType"] == "application/vnd.google-apps.folder":
                    files.extend(self.folder_contents(file["id"]))
                    # drop file from files
                    files.remove(file)
        return files
    
    def folder_contents(self, folder_id):
        """Return all files in a folder and subfolders
        """
        return self.drive_request(f"'{folder_id}' in parents", recursive=True)

    def list_folders(self):
        """List all folders in drive
        """
        return self.drive_request("mimeType = 'application/vnd.google-apps.folder'")
        

    def search_folder(self, folder_name:str) -> list:
        """Search for a folder by name
        """
        return self.drive_request(f"name contains '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'")

    def download_file(self, file_id:str) -> io.BytesIO:
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        """
        
        try:

            # pylint: disable=maybe-no-member
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')
            return file.getvalue()
        
        except HttpError as error:
            print(F'An error occurred: {error}')        
    



