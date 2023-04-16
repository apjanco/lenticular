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
# Helful: https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/drive_v2.files.html

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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
                    #TODO not actually recursive, only one level deep
                    # Better to get all folders and then iterate through them
                    # drop file from files
                    files.remove(file)
        return files
    
    def folder_contents(self, folder_id):
        """Return all files in a folder and its subfolders
        """
        return self.drive_request(f"'{folder_id}' in parents", recursive=True)

    def list_folders(self):
        """List all folders in drive
        """
        return self.drive_request("mimeType = 'application/vnd.google-apps.folder'")
        
    def search(self, query:str) -> list:
        """Search using the query syntax https://developers.google.com/drive/api/guides/search-files#examples
        """
        return self.drive_request(f"{query}")

    def search_folders(self, folder_name:str) -> list:
        """Search for a folder by name
        """
        return self.drive_request(f"name contains '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'")

    def search_files(self, query:str) -> list:
        """Search for a file by name
        """
        return self.drive_request(f"name contains '{query}' and mimeType != 'application/vnd.google-apps.folder'")

    def get_file_by_id(self, file_id:str) -> list:
        """Search for a file by ID
        """
        return self.service.files().get(fileId=file_id).execute()


    def download_file(self, file_id:str) -> io.BytesIO:
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        """
        #TODO Need to first get file mimeType 
        file_data = self.get_file_by_id(file_id)
        kind = file_data.get('kind')
        mimeType = file_data.get('mimeType')
        name = file_data.get('name')
        # Google Docs and Sheets throw: Only files with binary content can be downloaded. Use Export with Docs Editors files.
        
        if mimeType == "application/vnd.google-apps.document":
            request = self.service.files().export_media(fileId=file_id, mimeType='application/pdf')
        if mimeType == "application/vnd.google-apps.spreadsheet":
            request = self.service.files().export_media(fileId=file_id, mimeType='application/pdf')
        if mimeType == "application/vnd.google-apps.presentation":
            request = self.service.files().export_media(fileId=file_id, mimeType='application/pdf')
        if mimeType == "application/vnd.google-apps.drawing":
            request = self.service.files().export_media(fileId=file_id, mimeType='image/png')
        if mimeType == "application/vnd.google-apps.form":
            request = self.service.files().export_media(fileId=file_id, mimeType='application/pdf')            
        else:
            request = self.service.files().get_media(fileId=file_id)

        try:
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')
            return file.getvalue()
        
        except HttpError as error:
            if error.status_code == 403:
                print(f'A permission error occurred: {error}')
                #also error.reason == appNotAuthorizedToFile
                #TODO, this error occures with all files, can I create a copy and download that?
            else:
                print(f'An error occurred: {error}')        
    



