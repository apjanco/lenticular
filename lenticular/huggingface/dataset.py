import srsly
from pathlib import Path
from datasets import load_dataset


def gen(file_path: Path):
    for file in file_path.iterdir():
        if file.is_file():
            yield {"path": str(file), "name": file.name}


def create_metadata(project_path: Path):
    metadata = {}
    srsly.write_jsonl((project_path / "metadata.jsonl"), metadata)


def create_dataset(file_path: Path, dataset_name: str = "dataset"):
    # TODO, how to work with all file formats? Also how does this work?
    # https://huggingface.co/docs/datasets/package_reference/main_classes
    ds = load_dataset("imagefolder", data_dir=file_path)
    dataset = load_dataset("json", data_files="datasets-issues.jsonl", split="train")
    # a = gen(file_path)
    # ds = Dataset.from_generator(a)
    # ds.save_to_disk(dataset_name)
    return ds


# 1 add file binary to dataset, currently only works with images and audio, but we can make our own

# existing image https://sourcegraph.com/github.com/huggingface/datasets/-/blob/src/datasets/packaged_modules/imagefolder/imagefolder.py
from datasets.packaged_modules.folder_based_builder import folder_based_builder


class FolderBuilderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for Folder."""

    drop_labels: bool = None
    drop_metadata: bool = None


class FolderBuilder(folder_based_builder.FolderBasedBuilder):
    """
    BASE_FEATURE: feature object to decode data (i.e. datasets.Image(), datasets.Audio(), ...)
    BASE_COLUMN_NAME: string key name of a base feature (i.e. "image", "audio", ...)
    BUILDER_CONFIG_CLASS: builder config inherited from `folder_based_builder.FolderBasedBuilderConfig`
    EXTENSIONS: list of allowed extensions (only files with these extensions and METADATA_FILENAME files
            will be included in a dataset)
    CLASSIFICATION_TASK: classification task to use if labels are obtained from the folder structure
    https://sourcegraph.com/github.com/huggingface/datasets/-/blob/src/datasets/packaged_modules/folder_based_builder/folder_based_builder.py
    """

    BUILDER_CONFIG_CLASS = FolderBuilderConfig
    EXTENSIONS = ["jpg", "jpeg", "png", "bmp", "wav", "mp3", "flac", "txt"]
    BASE_FEATURE = None  # TODO does this allow multiple base features? Only image and audio features currently supported
    """
    import pyarrow as pa
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    """

    BASE_COLUMN_NAME = None
    METADATA_FILENAME = "metadata.jsonl"


# 2 use Repository class to push to hub https://huggingface.co/docs/huggingface_hub/v0.8.1/en/how-to-upstream
