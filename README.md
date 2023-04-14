# lenticular
😶‍🌫️ A set of tools for fetching files from the cloud

We often work with partners who have materials stored in cloud services like Google Drive and Box.  This is a library for accessing those materials. This allows partners to continue using familiar technologies to manage their data, while developers can fetch or sync data for projects. 

# Usage

`get_gdrive_service()` 
Creates a service object for requests to the Google Drive API

`list_all_files(folder=None)`
Lists all files in a given drive. Returns a list of ids that can be used to download the files.

`folder_contents(service, folder_id)`
Get all the files in a given folder
#Lists all files and folders in a folder
#TODO recursive search down subfolders

`search_file(service, query)`
Search for files in Drive with a given query. Reurns a list of file ids that can be downloaded

`search_folder(service, folder_name)`
Search for a folder with a given name

`download_file(service, real_file_id)`
Downloads the data of a specific file give its id


Need to: 

- Connect to Drive service
- Fetch all files in a given directory

List files 
`service.files().list()`
Save a file to a new format
`service.files().export_media(fileId=file_id, mimeType='application/pdf')`
