import os
import re
from rich import print
import unicodedata
from pathlib import Path

###
# Helper functions from django.utils.text.py
###


def get_valid_filename(name):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    if s in {"", ".", ".."}:
        print("Could not derive file name from '%s'" % name)
    return s


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


class Filenames:
    """
    Load and normalize the names of all directories and files.

    """

    def __init__(self, paths: list):
        self.normalize(paths)

    def normalize(self, paths: list):
        new_paths = []
        for path in paths:
            if Path(path).exists():
                for root, dirs, files in os.walk(path, topdown=False):
                    # Change file names if needed
                    for name in files:
                        # check file permissions
                        if not os.access(os.path.join(root, name), os.W_OK):
                            # change file permissions
                            os.chmod(os.path.join(root, name), 0o777)
                        # for each file in the directory run get_valid_filename
                        valid_name = get_valid_filename(name)
                        if name != valid_name:
                            # if the file name is not valid, rename it
                            os.rename(
                                os.path.join(root, name), os.path.join(root, valid_name)
                            )
                    # Change subdirectory names if needed
                    for name in dirs:
                        if not os.access(os.path.join(root, name), os.W_OK):
                            # change file permissions
                            os.chmod(os.path.join(root, name), 0o777)
                        valid_name = "/".join(
                            [
                                get_valid_filename(part)
                                for part in name.split("/")
                                if part
                            ]
                        )
                        new_paths.append(os.path.join(root, valid_name))
                        if name != valid_name:
                            # if the file name is not valid, rename it
                            Path(os.path.join(root, name)).rename(
                                os.path.join(root, valid_name)
                            )
                # Change root directory name if needed
                # NOTE this comes last because it corrupts all the existing paths
                if not os.access(os.path.join(path), os.W_OK):
                    # change file permissions
                    os.chmod(os.path.join(path), 0o777)
                    # for each file in the directory run get_valid_filename
                valid_root = "/" + "/".join(
                    [get_valid_filename(part) for part in path.split("/") if part]
                )

                new_paths = [p.replace(path[:-1], valid_root) for p in new_paths]
                new_paths.append(valid_root)

                if path != valid_root:
                    # if the file name is not valid, rename it
                    Path(os.path.join(path)).rename(os.path.join(valid_root))
            else:
                print("Path does not exist: ", path)

        self.paths = new_paths
