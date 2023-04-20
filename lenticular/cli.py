import typer 

app = typer.Typer()

@app.command()
def download_folder(folder_id: str):
    print(f"Downloading folder {folder_id}")

