import os
import requests 
import yaml
from pathlib import Path
from boxsdk import Client, OAuth2

# Go to
#https://developer.box.com/guides/cli/quick-start//
#https://developer.box.com/guides/cli/quick-start/create-oauth-app/
# note that developer token is only valid for 60 minutes
BOX_CLIENT_ID = os.environ.get('BOX_CLIENT_ID')
BOX_CLIENT_SECRET = os.environ.get('BOX_CLIENT_SECRET')
BOX_DEVELOPER_TOKEN = os.environ.get('BOX_DEVELOPER_TOKEN')



def read_policies():
    with open('policies.yaml', 'r') as file:
        policies = yaml.safe_load(file)
    return policies

def get_box_client():
    if BOX_CLIENT_ID and BOX_CLIENT_SECRET and BOX_DEVELOPER_TOKEN:
        auth = OAuth2(
            client_id=BOX_CLIENT_ID,
            client_secret=BOX_CLIENT_SECRET,
            access_token=BOX_DEVELOPER_TOKEN,
        )
        return Client(auth)
    else:
        print("Please set BOX_CLIENT_ID, BOX_CLIENT_SECRET, and BOX_DEVELOPER_TOKEN environment variables")


class Box:
    """
    Instantiate a Box session.
    
    """

    def __init__(self):
        self.client = get_box_client()
        self.policies = read_policies()

    
    def folder_contents(self, folder_id:str):
        """Return all files in a folder and its subfolders"""
        contents = []
        folder = self.client.folder(folder_id).get_items()
        for item in folder:
            if item.type == 'folder':
                self.folder_contents(item.id)
            elif item.type == 'file':
                contents.append({'name':item.name, 'id':item.id, 'download_url':item.get_download_url()})
            print(f'{item.type.capitalize()} {item.id} is named "{item.name}"')
    
    def search(self, query:str):
        """Search for files in box"""
        return self.client.search().query(query=query).get()
    
    def download_file(self, file_id:str, path: str = None):
        """Download a file from box"""
        metadata = self.client.file(file_id=file_id).get_all_metadata()
        print(f'Got metadata instance {metadata["$id"]}')
        f = self.client.file(file_id).get()
        url = f.get_download_url()
        file = requests.get(url)
        Path(path + f.name).with_suffix(suffix).write_bytes(file.content)

    