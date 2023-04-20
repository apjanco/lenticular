import typer 
import yaml
from pathlib import Path
from typing import List
from rich import print
from .drive import Drive
from .normalize import Filenames, Images
from .huggingface.dataset import create_dataset
app = typer.Typer()
#load policies
policies = yaml.safe_load((Path.cwd() / "policies.yaml").read_text())

@app.command()
def meep():
    """
    Meep meep!
    """
    # 

    typer.echo(" Meep!")

@app.command()
def download(id: str = typer.Argument(..., help="Google Drive ID")):
    if id:
        drive = Drive()
        data = drive.get_file_by_id(id)
        if data["mimeType"] and data["mimeType"] == "application/vnd.google-apps.folder":
            success = drive.download_folder(id)
            print(f"🤩 Downloaded to {policies['output_path']}/{success}")
        else:
            success = drive.download_file(id)
            Path(f"{policies['output_path']}/{success['name']}{success['suffix']}").write_bytes(success['content'])
            print(f"🤩 Downloaded to {policies['output_path']}/{success['name']}{success['suffix']}")
    else:            
        print("""🚩 [bold red]No Google Drive id provided.[/bold red]\n
The File ID can be found in the URL of the file when it is opened on Google Drive. It is the combination of letters and numbers that appear after "d/" in the link: 
https://docs.google.com/spreadsheets/d/[bold green]1vKx1iPAplNzydYZbFEAxLknpR8S6UzjC91sAXTrpVVw[/bold green]/edit#gid=123456789
For example, in the URL above the File ID is "1vKx1iPAplNzydYZbFEAxLknpR8S6UzjC91sAXTrpVVw""")

@app.command()
def normalize(paths:List[Path] = typer.Argument(None, help="Paths on your machine to normalize.")):
    if not paths:
        paths = [policies['output_path']]
    Filenames(paths) #TODO add tag to run or not run this
    Images(paths) #TODO add tag to run or not run this
    print(paths)

@app.command()
def dataset(path: Path = typer.Argument(None, help="Transform a folder of images into a dataset."), dataset_name: str = typer.Option('dataset', help="Name of the dataset to create.")):
    if not path:
        path = Path(policies['output_path'])
    create_dataset(path, dataset_name)

@app.command()
def publish(dataset_path: str = typer.Argument(..., help="Dataset to publish.")):
    print(dataset_path)
