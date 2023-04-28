We often work with partners who have materials stored in cloud services like Google Drive and Box.  This is a library for accessing those materials. This allows partners to use familiar technologies to manage their data, while developers can fetch and normalize data for projects. 

# Installation

```
pip install lenticular
```

```
git clone https://github.com/apjanco/lenticular.git

cd lenticular

# If you need to install Poetry
curl -sSL https://install.python-poetry.org | python3 -

poetry install
```

# Basic Usage

1. [Set API keys for Drive and/or Box](./secrets)

2. [Create a project and set the file policies](./policies).

3. Google Drive  

    `$ lenticular drive-download 1R8JA-C_QxSdekKfRfetj5j4fbjFXJu6G`  
    or
    ```python 
    from lenticular.drive import Drive 

    drive = Drive() 

    drive.download_folder('1R8JA-C_QxSdekKfRfetj5j4fbjFXJu6G')
    ```

    > more on [Drive](./drive)

4. Box 

    `$ lenticular box-download 160107962928`  
    or
    ```python 
    from lenticular.box import Box

    client = Box() 

    client.download_folder('160107962928')
    ```

    > more on [Box](./box)

