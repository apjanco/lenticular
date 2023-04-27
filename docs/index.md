# Get Started
Fetch files from the cloud

We often work with partners who have materials stored in cloud services like Google Drive and Box.  This is a library for accessing those materials. This allows partners to continue using familiar technologies to manage their data, while developers can fetch or sync data for projects. 

# Installation

```
$ pip install lenticular
```

For Drive, generate a `credentials.json` file using [these instructions.]( https://developers.google.com/drive/api/quickstart/python) 

# Basic Usage

1. [Set API keys for Drive and/or Box](./secrets)

2. [Create a project and set the file policies](./policies).

3. Then for Google Drive

    ```python 
    from lenticular.drive import Drive 

    drive = Drive() 

    drive.download_folder('1R8JA-C_QxSdekKfRfetj5j4fbjFXJu6G')
    ```

    > more on [Drive](./drive)

4. Or for Box 

    ```python 
    from lenticular.box import Box

    client = Box() 

    client.download_folder('160107962928')
    ```

    > more on [Box](./box)

