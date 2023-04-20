from pathlib import Path 
import yaml
from typing import Optional
import os
import filetype
from PIL import Image


policies = yaml.safe_load((Path.cwd() / "lenticular"/ "policies.yaml").read_text())

###
# Helper functions for image normalization
###

#This section changes the size of an image file if it is larger than a given size
#https://stackoverflow.com/questions/13407717/python-image-library-pil-how-to-compress-image-into-desired-file-size
class file_counter(object):
    def __init__(self):
        self.position = self.size = 0

    def seek(self, offset, whence=0):
        if whence == 1:
            offset += self.position
        elif whence == 2:
            offset += self.size
        self.position = min(offset, self.size)

    def tell(self):
        return self.position

    def write(self, string):
        self.position += len(string)
        self.size = max(self.size, self.position)

def smaller_than(im, size, guess=70, subsampling=1, low=1, high=100):
    while low < high:
        counter = file_counter()
        im.save(counter, format='JPEG', subsampling=subsampling, quality=guess)
        if counter.size < size:
            low = guess
        else:
            high = guess - 1
        guess = (low + high + 1) // 2
    return low

def is_image(file):
    """Leaves the png and webp alone"""
    kind = filetype.guess(str(file))
    if kind.mime == 'image/jpeg':
        return True

    elif kind.mime == 'image/gif':
        im = Image.open(str(file))
        im = im.convert('RGB')
        im.save(str(file), "JPEG", quality=100)
        return True

    elif kind.mime == 'image/tiff':
        im = Image.open(str(file))
        im = im.convert("RGB")
        im.save(str(file), "JPEG", quality=100)
        return True

    else:
        return False

def change_size_if_needed(file:Path, size:int, out_path:str):
    if is_image(file):
        if os.path.getsize(str(file)) > size:
            
            im = Image.open(file)
            size = smaller_than(im, size)
            if out_path:
                im.save((out_path / file.name), 'JPEG', quality=size)
            else:
                im.save(file, 'JPEG', quality=size)
        else:
            pass


###
# Class for image normalization
###

class Images:
    """
    Load and normalize a directory of images.

    """

    def __init__(self):
        self.paths: list[Path] = []
        self.output_path = policies["output_path"]
        self.image_output_format = policies["images"]["output_format"]
        self.image_output_size = policies["images"]["output_size"]
        self.output_size = (0, 0)
        self.output_mode = "RGB"
        self.output_quality = 100
        self.output_prefix = ""
        self.output_suffix = ""


    def resize_images(self):
        for file in self.image_paths:
            change_size_if_needed(file, self.image_output_size, self.output_path)