We often work with partners who have materials stored in cloud services like Google Drive and Box.  This is a library for accessing those materials. This allows partners to use familiar technologies to manage their data, while developers can fetch and normalize data for projects. 

# Installation

```bash 
git clone https://github.com/apjanco/lenticular.git
cd lenticular 
```
Install poetry if you don't have it: 
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
then 
```bash
poetry shell  # create a virtual environment
poetry install # install dependencies
lenticular 
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

