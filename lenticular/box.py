import os
import requests
import yaml
from pathlib import Path
import boxsdk
from boxsdk import Client, OAuth2
from tqdm import tqdm
import asyncio
import aiofiles
import aiohttp
from rich import print

# Go to
# https://developer.box.com/guides/cli/quick-start//
# https://developer.box.com/guides/cli/quick-start/create-oauth-app/
# note that developer token is only valid for 60 minutes


def read_policies():
    with open("./lenticular/policies.yaml", "r") as file:
        policies = yaml.safe_load(file)
    return policies


def get_box_client():
    BOX_CLIENT_ID = os.environ.get("BOX_CLIENT_ID")
    BOX_CLIENT_SECRET = os.environ.get("BOX_CLIENT_SECRET")
    BOX_DEVELOPER_TOKEN = os.environ.get("BOX_DEVELOPER_TOKEN")
    if BOX_CLIENT_ID and BOX_CLIENT_SECRET and BOX_DEVELOPER_TOKEN:
        auth = OAuth2(
            client_id=BOX_CLIENT_ID,
            client_secret=BOX_CLIENT_SECRET,
            access_token=BOX_DEVELOPER_TOKEN,
        )
        client = Client(auth)
        try:
            client.user().get()
            return client
        except boxsdk.exception.BoxOAuthException:
            print(
                "[orange_red1]Developer token is only valid for 60 minutes. Please get a new one at https://upenn.app.box.com/developers/console[/orange_red1]"
            )
    else:
        print(
            "Please set BOX_CLIENT_ID, BOX_CLIENT_SECRET, and BOX_DEVELOPER_TOKEN environment variables"
        )


class Box:
    """
    Instantiate a Box session.

    """

    def __init__(self):
        self.client = get_box_client()
        self.policies = read_policies()

    # def download_folder(self, folder_id:str):
    #    asyncio.run(self.download_folder_coroutine(folder_id))

    def download_folder(self, folder_id: str):
        """Download all files in a folder and its subfolders"""
        if self.policies and self.policies["output_path"]:
            output_path = self.policies["output_path"]
            if not output_path.endswith("/"):
                output_path = output_path + "/"
        contents = self.folder_contents(folder_id)

        # Get all folders and create them if they don't exist
        folders = set([i["path"] for i in contents])
        for folder in folders:
            save_path = Path(output_path + folder)
            if not save_path.exists():
                save_path.mkdir(parents=True)

        async def fetch_file(item: dict):
            # https://gist.github.com/darwing1210/c9ff8e3af8ba832e38e6e6e347d9047a
            sema = asyncio.BoundedSemaphore(5)
            async with sema, aiohttp.ClientSession() as session:
                async with session.get(item["download_url"]) as resp:
                    assert resp.status == 200
                    data = await resp.read()

            async with aiofiles.open(
                os.path.join(output_path, item["path"], item["name"]), "wb"
            ) as outfile:
                pbar.update(1)
                await outfile.write(data)

        # TODO add progress bar
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(fetch_file(f)) for f in contents]
        pbar = tqdm(total=len(contents), desc="Downloading files")
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    def folder_contents(self, folder_id: str):
        """Return all files in a folder and its subfolders. Useful to get list of files without downloading them.
        Args:
            folder_id: str
        Returns:
            contents: list of dicts
        """
        contents = []
        folder = self.client.folder(folder_id).get_items()
        for item in folder:
            if item.type == "folder":
                contents.extend(self.folder_contents(item.id))
            elif item.type == "file":
                item = item.get()
                file_path = "/".join(f.name for f in item.path_collection["entries"])
                contents.append(
                    {
                        "name": item.name,
                        "id": item.id,
                        "download_url": item.get_download_url(),
                        "path": file_path,
                    }
                )
        return contents

    def search(self, query: str):
        """Search for files in box"""
        return [i for i in self.client.search().query(query=query)]

    def download_file(self, file_id: str, path: str = None):
        """Download a file from box"""
        f = self.client.file(file_id).get()
        Path(path + f.name).write_bytes(f.content())
