import enum
from os import path


class FileExtensionEnum(enum.Enum):
    wav = '.wav'


def check_extension(filepath) -> bool:
    full_name = path.basename(filepath)
    ext = path.splitext(full_name)[1]
    for e in FileExtensionEnum:
        if e.value != ext:
            return False
        return True


def format_filename(filepath) -> str:
    full_name = path.basename(filepath)
    name = path.splitext(full_name)[0]
    return name + '.mp3'
