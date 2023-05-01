import srsly
from pathlib import Path
from datasets import load_dataset
from huggingface_hub.hf_api import HfApi
from rich import print 

def gen(file_path: Path):
    for file in file_path.iterdir():
        if file.is_file():
            yield {"path": str(file), "name": file.name}


def create_metadata():
    policies = srsly.read_yaml("./lenticular/policies.yaml")
    folder_path = policies.get("output_path", None)
    metadata = {}
    srsly.write_jsonl(f"{folder_path}/metadata.jsonl", metadata)


def create_dataset(dataset_name: str = "dataset", private: bool = True):
    """
    Create a dataset from a folder of files.
    https://github.com/huggingface/huggingface_hub/tree/main/src/huggingface_hub#publish-files-to-the-hub
    """
    policies = srsly.read_yaml("./lenticular/policies.yaml")
    folder_path = policies.get("output_path", None)
    if folder_path:
        api = HfApi()
        print(f"[green]Creating dataset {dataset_name}[/green]")
        create_metadata()
        api.create_repo(private=private, repo_id=dataset_name, repo_type="dataset")
        api.upload_folder(folder_path=folder_path, repo_id=dataset_name, repo_type="dataset")
        print(f"🐬 Dataset created! You can find it at https://huggingface.co/datasets/{dataset_name}")
    else:
        print("Please set output_path in policies.yaml by running: $ lenticular policies")

# Serve assets from HF? https://huggingface.co/datasets/ajanco/testing/resolve/main/Is_Folder/Checkout%20%E2%80%93%20VividSeats.com.pdf
# NO does not work for LFS files 