import os

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    UploadFile,
    File)
from fastapi.responses import FileResponse
from pydantic import ValidationError
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from db.models import User, Record
from db.session import get_session
from .schemas import (
    UserCreateRequest,
    UserCreateResponse,
    RecordCreateResponse)
from settings import (
    HOST,
    PORT,
    WAV_UPLOADED_FILES,
    MP3_UPLOADED_FILES)
from .helpers import (
    check_extension,
    save_file_to_uploads_async,
    convert_file_async)

router = APIRouter(prefix='/api/v1')


@router.post('/users', tags=['Create user'], response_model=UserCreateResponse)
async def create_user(
        request: UserCreateRequest,
        session: AsyncSession = Depends(get_session)):
    try:
        user = User(
            name=request.name,
            token=str(uuid4()),
            email=request.email
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The data are not valid.'
        )
    query = await session.execute(select(User).filter_by(email=request.email))
    result = query.first()
    if result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User email already exists.'
        )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    await session.close()
    return {'id': user.id, 'token': user.token}


@router.post('/records', tags=['Create record'], response_model=RecordCreateResponse)
async def create_record(
        user_id: int,
        token: str,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)):
    if not check_extension(file):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='File extension is not supported.'
        )
    query = await session.execute(select(User).filter_by(id=user_id, token=token))
    result = query.first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid user_id or token.'
        )
    record_id = str(uuid4())
    filename, ext = os.path.splitext(file.filename)
    old_filepath = WAV_UPLOADED_FILES + f'{record_id}{ext}'
    await save_file_to_uploads_async(file, old_filepath)
    input_path = fr'{old_filepath}'
    new_full_name = f'{record_id}.mp3'
    output_path = MP3_UPLOADED_FILES + new_full_name
    await convert_file_async(input_path, output_path)
    record = Record(id=record_id, file_name=new_full_name, orig_file_name=f'{filename}{ext}', owner=result[0])
    session.add(record)
    await session.commit()
    return {'url': f'http://{HOST}:{PORT}/record?id={record_id}&user={result[0].id}'}


@router.get('/record', tags=['Download record'])
async def get_record(
        id: str,
        user: int,
        session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(Record).filter_by(id=id, user_id=user))
    record = query.first()
    file_name = record[0].file_name
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Record not found.'
        )
    if not os.path.exists(MP3_UPLOADED_FILES + file_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found.'
        )
    return FileResponse(
        MP3_UPLOADED_FILES + file_name,
        media_type='audio/mpeg',
        filename=file_name
    )
