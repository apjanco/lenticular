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

# Get Started

1. Set project [policies](./policies) for file naming and normalization. 
    ```bash
    lenticular policies
    ```

2. Enter API keys for Drive and/or Box
    ```bash
    lenticular secrets
    ```

3. Download from [Drive](./drive) 
    ```bash
    lenticular drive-download 1R8JA-C_QxSdekKfRfetj5j4fbjFXJu6G
    ```

4. Download from [Box](./box)
    ```bash
    lenticular box-download 173302952002
    ```
5. Normalize files
    ```bash
    lenticular normalize
    ```

6. Create or update a dataset from files
    ```bash
    lenticular dataset
    ```

7. Add OCR text using Vision
    ```bash
    lenticular process
    ```

8. Push updated files and data to Huggingface Hub
    ```bash
    lenticular dataset
    ```


