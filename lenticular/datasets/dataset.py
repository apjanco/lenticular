from pathlib import Path
from datasets import Dataset

def gen(file_path:Path):
    for file in file_path.iterdir():
        if file.is_file():
            yield {"path": str(file), "name": file.name}
    

def create_dataset(file_path:Path, dataset_name:str = 'dataset'):
    ds = Dataset.from_generator(gen(file_path))
    ds.save_to_disk(dataset_name)
    return ds