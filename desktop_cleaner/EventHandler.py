import os
import shutil
from datetime import date, datetime
from pathlib import Path
from pytz import timezone
from watchdog.events import FileSystemEventHandler

from extensions import extension_paths


def add_date_to_file_name(filename):
    """
    Helper function that adds current datetime to the file name.

    :param Str source: source of file to be moved
    """
    _datestamp = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%m-%Y %I-%M-%S %p')
    filename = f"{filename.split('.')[0]}_{_datestamp}.{filename.split('.')[-1]}"
    return filename


def rename_file(source: str, destination_path: Path):
    """
    Helper function that renames file to reflect new path. If a file of the same
    name already exists in the destination folder, the file name is numbered and
    incremented until the filename is unique (prevents overwriting files).

    :param Str source: source of file to be moved
    :param Path destination_path: path to destination directory
    """
    if Path(destination_path / source).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / f'{source.split(".")[0]}_{increment}{source.split(".")[-1]}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source

def check_destination_path(destination_path):

    if not Path(destination_path).exists():
        destination_path.mkdir(parents=True, exist_ok=True)

class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        try:
            for child in self.watch_path.iterdir():
                if child.name == "holder of things":
                    continue
                # skips directories and non-specified extensions
                print('child', child)
                if child.suffix.lower() in extension_paths:
                # if child.is_file() and child.suffix.lower() in extension_paths:
                    destination_path = self.destination_root / extension_paths[child.suffix.lower()]
                    check_destination_path(destination_path)
                    filename = os.path.basename(child)
                    new_name = add_date_to_file_name(filename)
                    if extension_paths[child.suffix.lower()] != "other/uncategorized":
                        destination_path = rename_file(source=new_name, destination_path=destination_path)
                    shutil.move(src=child, dst=destination_path)
        except Exception as e:
            print(str(e))
            return str(e)
