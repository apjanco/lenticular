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
    results = drive.search_folders('folder name')
    ```

- Search for a file by name
    ```python
    results = drive.search_files('filename')
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


The error message "The user has not granted the app read access" suggests that the credentials used by your script do not have the necessary permissions to access and export the file.

To fix this, you need to ensure that your credentials have been authorized with the required scopes. Specifically, you need to make sure that you have authorized the `https://www.googleapis.com/auth/drive.readonly` scope. This scope allows your application to read the contents of a user's Google Drive.

Here's how you can authorize the required scope:

1. Go to the Google Cloud Console (https://console.cloud.google.com/)
2. Select your project, then navigate to the "Credentials" section.
3. Find the credential that you're using for your script (e.g., a Service Account or OAuth Client ID).
4. Click on "Edit" to open the configuration page for the credential.
5. Scroll down to the "Scopes" section, then click "Add Scopes".
6. Search for "Google Drive API", then select the `https://www.googleapis.com/auth/drive.readonly` scope.
7. Click "Update" to save the changes.

After authorizing the required scope, you may need to regenerate your credentials and/or re-run the authentication flow for your application to take effect.

Note that if you're using a Service Account, you'll also need to share the file/folder that you're trying to access with the email address associated with the Service Account. You can find the email address in the JSON key file for your Service Account.