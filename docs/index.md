# Get Started
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
