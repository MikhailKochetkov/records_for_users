import aiofile
import ffmpeg
import os

from fastapi import HTTPException, status

from settings import WAV_UPLOADED_FILES


allowed_extensions = {".wav"}


def check_extension(file) -> bool:
    ext = os.path.splitext(file.filename)[1]
    return ext in allowed_extensions


def new_format_filename(filepath) -> str:
    full_name = os.path.basename(filepath)
    name = os.path.splitext(full_name)[0]
    return name + '.mp3'


def format_filename(file):
    filename, ext = os.path.splitext(file.filename)
    return filename + ext


async def save_file_to_uploads_async(file, filename):
    async with aiofile.async_open(
            f'{WAV_UPLOADED_FILES}{filename}', "wb"
    ) as uploaded_file:
        file_content = await file.read()
        await uploaded_file.write(file_content)
        await uploaded_file.close()


async def convert_file_async(input_stream, output_stream):
    async with aiofile.async_open(input_stream, "rb") as f:
        await f.read()
    try:
        stream = ffmpeg.input(input_stream)
        stream = ffmpeg.output(stream, output_stream)
        ffmpeg.run(stream)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
