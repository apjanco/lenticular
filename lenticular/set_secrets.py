import os
import json
from rich import print


def set_secrets():
    secrets = [
        "HUGGINGFACE_TOKEN",
        "BOX_CLIENT_ID",
        "BOX_CLIENT_SECRET",
        "BOX_DEVELOPER_TOKEN",
    ]
    for secret in secrets:
        current_secret_value = os.environ.get(secret)
        if current_secret_value is None:
            print(
                f"{secret} is not set. Please set it by typing the following command in your terminal: export {secret}='your_secret_value'"
            )

    # check if credentials.jsons file exists
    print("Checking if Google credentials.json file exists...")
    if not os.path.exists("credentials.json"):
        print(
            "🚩 [bold red]No credentials.json file found.[/bold red]\n Please follow the instructions here:https://developers.google.com/drive/api/quickstart/python"
        )
        print("save the file to ", os.getcwd())
    else:
        print("[bold green]Looks good! credentials.json file found.[/bold green]")


if __name__ == "__main__":
    set_secrets()
