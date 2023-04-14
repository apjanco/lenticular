# lenticular
😶‍🌫️ A set of tools for fetching files from the cloud

We often work with partners who have materials stored in cloud services like Google Drive and Box.  This is a library for accessing those materials. This allows partners to continue using familiar technologies to manage their data, while developers can fetch or sync data for projects. 

# Installation

```
$ pip install lenticular
```

# Usage

```python 
from lenticular.drive import Drive 

drive = Drive() 
```

--- 
- List all folders 
    ```python
    folders = drive.list_folders()
    ```

- Search for a folder by name
    ```python
    results = drive.search_folder('folder name')
    ```

- Get a list of all the files in a folder and its subfolders
    ```python
    files = drive.folder_contents('folder_id')
    ```

- Fetch a file from Drive by id
    ```python
    file = drive.download_file('file_id')
    ```


```python
#TODO 
>>> f= drive.download_file('1l02dYiSJa3r5RWb9oj8pbQxrARjz379f')
An error occurred: <HttpError 403 when requesting 
https://www.googleapis.com/drive/v3/files/1l02dYiSJa3r5RWb9oj8pbQxrARjz379f?alt=media returned "The user has not granted the app 
894403265340 read access to the file 1l02dYiSJa3r5RWb9oj8pbQxrARjz379f.". Details: "[{'message': 'The user has not granted the 
app 894403265340 read access to the file 1l02dYiSJa3r5RWb9oj8pbQxrARjz379f.', 'domain': 'global', 'reason': 
'appNotAuthorizedToFile', 'location': 'Authorization', 'locationType': 'header'}]">

```