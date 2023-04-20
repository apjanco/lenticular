from pathlib import Path
from datasets import load_dataset

def gen(file_path:Path):
    for file in file_path.iterdir():
        if file.is_file():
            yield {"path": str(file), "name": file.name}
    

def create_dataset(file_path:Path, dataset_name:str = 'dataset'):
    #TODO, how to work with all file formats? Also how does this work?
    #https://huggingface.co/docs/datasets/package_reference/main_classes
    ds = load_dataset("imagefolder", data_dir=file_path)
    # a = gen(file_path)
    # ds = Dataset.from_generator(a)
    # ds.save_to_disk(dataset_name)
    return ds