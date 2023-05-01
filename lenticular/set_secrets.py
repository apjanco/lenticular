import os
from rich import print
import srsly
from pathlib import Path 


def set_secrets():
    if not Path("./lenticular/secrets.json").exists():
        secrets = {
            "HUGGINGFACE_TOKEN": None,
            "BOX_CLIENT_ID": None,
            "BOX_CLIENT_SECRET": None,
            "BOX_DEVELOPER_TOKEN": None,
            "GOOGLE_API_KEY": None,
        }
    else:
        secrets = srsly.read_json("./lenticular/secrets.json")
    
    for secret in secrets.keys():
        if secrets[secret] is None:
            # prompt user for input and set environment variable
            new_secret_value = input(f"Enter a value for {secret}: ")            
            if new_secret_value:
                secrets[secret] = new_secret_value
                print(f"{secret}={new_secret_value}")
            else:
                print(
                    f"[bold red]No value entered for {secret}.[/bold red]"
                )
        else:
            # display current value as default, prompt user for input and set environment variable
            new_secret_value = input(f"Enter a value for {secret} (current is {secrets[secret]}): ")
            if new_secret_value == "":
                secrets[secret] = secrets[secret]
            else:
                secrets[secret] = new_secret_value
    srsly.write_json("./lenticular/secrets.json", secrets)
    print("☺️  [bold green] secrets.json file written.[/bold green]")
    
    # check if credentials.jsons file exists
    print("Checking if Google credentials.json file exists...")
    if not os.path.exists("./lenticular/credentials.json"):
        print(
            "🚩 [bold red]No credentials.json file found.[/bold red]\n Please follow the instructions here:https://developers.google.com/drive/api/quickstart/python"
        )
        # download credentials.json file
        new_secret_value = input(f"Paste the contents of your credentials.json file here: ")    
        if new_secret_value:
            srsly.write_json("./lenticular/credentials.json", new_secret_value)
        else:
            print(
                f"[bold red]No value entered for credentials.json.[/bold red]"
            )
    else:
        print("[bold green]Looks good! credentials.json file found.[/bold green]")
