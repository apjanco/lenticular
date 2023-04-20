import typer 
import yaml
from pathlib import Path
from rich import print
from .drive import Drive
app = typer.Typer()
#load policies
policies = yaml.safe_load((Path.cwd() / "policies.yaml").read_text())

@app.command()
def meep():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")

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