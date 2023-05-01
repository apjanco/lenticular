import typer
import srsly
from pathlib import Path
from typing import List
from rich import print
from .drive import Drive
from .box import Box
from .normalize import Filenames, Images
from .huggingface.dataset import create_dataset
from .set_policies import update_policies
from .set_secrets import set_secrets
app = typer.Typer()
# load policies

@app.command()
def meep():
    """
    Meep meep!
    """
    #

    typer.echo(" Meep!")


@app.command()
def drive_download(id: str = typer.Argument(..., help="Google Drive ID")):
    "Download a file or folder from Drive. Requires an ID"
    policies = srsly.read_yaml("./lenticular/policies.yaml")

    if id:
        drive = Drive()
        data = drive.get_file_by_id(id)
        if (
            data["mimeType"]
            and data["mimeType"] == "application/vnd.google-apps.folder"
        ):
            success = drive.download_folder(id)
            print(f"🤩 Downloaded to {policies['output_path']}/{success}")
        else:
            success = drive.download_file(id)
            Path(
                f"{policies['output_path']}/{success['name']}{success['suffix']}"
            ).write_bytes(success["content"])
            print(
                f"🤩 Downloaded to {policies['output_path']}/{success['name']}{success['suffix']}"
            )
    else:
        print(
            """🚩 [bold red]No Google Drive id provided.[/bold red]\n
The File ID can be found in the URL of the file when it is opened on Google Drive. It is the combination of letters and numbers that appear after "d/" in the link: 
https://docs.google.com/spreadsheets/d/[bold green]1vKx1iPAplNzydYZbFEAxLknpR8S6UzjC91sAXTrpVVw[/bold green]/edit#gid=123456789
For example, in the URL above the File ID is "1vKx1iPAplNzydYZbFEAxLknpR8S6UzjC91sAXTrpVVw"""
        )

@app.command()
def policies():
    "Update current policies."
    config = update_policies()
    if config:
        print("🤩 Policies updated!")

@app.command()
def secrets():
    "Update current secret settings."
    config = set_secrets()
    if config:
        print("🤩 Secrets updated!")

@app.command()
def box_download(id: str = typer.Argument(..., help="Box ID")):
    "Download a file or folder from Box. Requires an ID"
    if id:
        client = Box()
        client.download_folder(id)

    else:
        print("""🚩 [bold red]No Box id provided.[/bold red]\n""")


@app.command()
def normalize(
    paths: List[Path] = typer.Argument(None, help="Paths on your machine to normalize.")
):
    policies = srsly.read_yaml("./lenticular/policies.yaml")
    if not paths:
        paths = [policies["output_path"]]
    Filenames(paths)  # TODO add tag to run or not run this
    Images(paths)  # TODO add tag to run or not run this
    print(paths)


@app.command()
def dataset():
    create_dataset()


@app.command()
def publish(dataset_path: str = typer.Argument(..., help="Dataset to publish.")):
    print(dataset_path)
