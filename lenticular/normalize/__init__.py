from .filenames import Filenames
from .images import Images   

class Normalizer:
    
    def __init__(self, paths: list[str]):
        if not isinstance(paths, list):
            # raise an error
            raise TypeError("paths must be a list")
        self.filenames = Filenames(paths)
        #self.images = Images()

    