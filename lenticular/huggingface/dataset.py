import srsly
from pathlib import Path
from datasets import load_dataset
import huggingface_hub
from huggingface_hub.hf_api import HfApi
from rich import print 

def gen(file_path: Path):
    for file in file_path.iterdir():
        if file.is_file():
            yield {"path": str(file), "name": file.name}


def create_metadata():
    policies = srsly.read_yaml("./lenticular/policies.yaml")
    folder_path = policies.get("output_path", None)
    metadata = []
    for f in Path(folder_path).glob("*"):
        if f.is_file():
            metadata.append({"path": str(f), "name": f.name})

    srsly.write_jsonl(f"{folder_path}/metadata.jsonl", metadata)

def update_metadata():
    return {}

def create_dataset():
    """
    Create a dataset from a folder of files.
    https://github.com/huggingface/huggingface_hub/tree/main/src/huggingface_hub#publish-files-to-the-hub
    
    """
    policies = srsly.read_yaml("./lenticular/policies.yaml")
    dataset_name = policies["dataset_name"]
    huggingface_org = policies["huggingface_org"]
    dataset_name = f"{huggingface_org}/{dataset_name}"
    private = policies.get("private_repo", True)

    folder_path = policies.get("output_path", None)
    if folder_path:
        api = HfApi()
        try:
            # Repository exists
            info = api.dataset_info(dataset_name)
            api.upload_folder(
                folder_path=folder_path,
                repo_id=dataset_name,
                repo_type="dataset",
            )
            print(f"🐬 Dataset updated!")

        except huggingface_hub.utils._errors.RepositoryNotFoundError:
            # Repository does not exist, create it and upload
            create_metadata()
            api.create_repo(private=private, repo_id=dataset_name, repo_type="dataset")
            api.upload_folder(folder_path=folder_path, repo_id=dataset_name, repo_type="dataset")
            print(f"🐬 Dataset created! You can find it at https://huggingface.co/datasets/{dataset_name}")
    else:
        print("Please set output_path in policies.yaml by running: $ lenticular policies")

# Serve assets from HF? https://huggingface.co/datasets/ajanco/testing/resolve/main/Is_Folder/Checkout%20%E2%80%93%20VividSeats.com.pdf
# NO does not work for LFS files 