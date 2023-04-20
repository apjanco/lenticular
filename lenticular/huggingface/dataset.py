from pathlib import Path
from datasets import Dataset

def gen(file_path:Path):
    for file in file_path.iterdir():
        if file.is_file():
            yield {"path": str(file), "name": file.name}
    

def create_dataset(file_path:Path, dataset_name:str = 'dataset'):
    a = gen(file_path)
    ds = Dataset.from_generator(a)
    ds.save_to_disk(dataset_name)
    return ds