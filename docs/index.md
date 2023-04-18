# 😶‍🌫️ lenticular
Fetch files from the cloud

We often work with partners who have materials stored in cloud services like Google Drive and Box.  This is a library for accessing those materials. This allows partners to continue using familiar technologies to manage their data, while developers can fetch or sync data for projects. 

# Installation

```
$ pip install lenticular
```

For Drive, generate a `credentials.json` file using [these instructions.]( https://developers.google.com/drive/api/quickstart/python) 

# Usage

```python 
from lenticular.drive import Drive 

drive = Drive() 
```

--- 

- Download a file
    ```python 
    f = drive.download_file('10HCqZH88PUr_19-A__GllqOk4srH_ikDbrwSnQhJYUw')
    ```
    
- Download a folder, (all files and subfolders)
    ```python 
    drive.download_folder('1R8JA-C_QxSdekKfRfetj5j4fbjFXJu6G')
    ```


Links:
https://docs.iterative.ai/PyDrive2/

I am not sure that I should add sync. 
1. No sync. We fetch all project assets.
- we then manage them in a new enviornment
- partners need to learn this new enviornment 
- we are able to clean and process materials, save them to a proper dataset 

2. Sync. We fetch and update from the cloud
- partners maintain in familiar env
- we'd need to clean and process materials in the cloud

3. Two sets. We fetch from the cloud, clean, then push cleaned new version back to cloud, run sync on new version.
- presumes need to track updates (how often will it change?)
- partners maintain in familiar env
- we don't have to pay for storage (new version acts as data store)
- people will continue to add stuff, and they'll add it where they know
