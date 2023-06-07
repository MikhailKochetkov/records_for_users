import enum
import ffmpeg
import os
from fastapi import HTTPException, status

from settings import WAV_UPLOADED_FILES


class FileExtensionEnum(enum.Enum):
    wav = '.wav'


def check_extension(file) -> bool:
    ext = os.path.splitext(file.filename)[1]
    for e in FileExtensionEnum:
        if e.value != ext:
            return False
        return True


def new_format_filename(filepath) -> str:
    full_name = os.path.basename(filepath)
    name = os.path.splitext(full_name)[0]
    return name + '.mp3'


def format_filename(file):
    filename, ext = os.path.splitext(file.filename)
    return filename + ext


async def save_file_to_uploads(file, filename):
    with open(f'{WAV_UPLOADED_FILES}{filename}', "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()


def convert_file(in_stream, out_stream):
    with open(in_stream, "rb") as f:
        f.read()
    try:
        stream = ffmpeg.input(in_stream)
        stream = ffmpeg.output(stream, out_stream)
        ffmpeg.run(stream)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
