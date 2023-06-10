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
from sqlalchemy.orm import Session
from uuid import uuid4

from db.models import User, Record
from db.session import get_db
from .schemas import (
    UserCreateRequest,
    UserCreateResponse,
    RecordCreateResponse)
from settings import (
    HOST,
    PORT,
    WAV_UPLOADED_FILES,
    MP3_UPLOADED_FILES)
from .file_handlers import (
    check_extension,
    save_file_to_uploads_async,
    convert_file_async)

router = APIRouter()


@router.post("/users", tags=["Create user"], response_model=UserCreateResponse)
async def create_user(
        request: UserCreateRequest,
        session: Session = Depends(get_db)):
    try:
        user = User(
            name=request.name,
            token=str(uuid4()),
            email=request.email
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The data are not valid."
        )
    if session.query(User).filter_by(email=request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User email already exists."
        )
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return {"id": user.id, "token": user.token}


@router.post("/records", tags=["Create record"], response_model=RecordCreateResponse)
async def create_record(
        user_id: int,
        token: str,
        file: UploadFile = File(...),
        session: Session = Depends(get_db)):
    if not check_extension(file):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File extension is not supported."
        )
    user = session.query(User).filter_by(id=user_id, token=token).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user_id or token."
        )
    record_id = str(uuid4())
    filename, ext = os.path.splitext(file.filename)
    old_filepath = WAV_UPLOADED_FILES + f'{record_id}{ext}'
    await save_file_to_uploads_async(file, old_filepath)
    input_path = fr"{old_filepath}"
    new_full_name = f'{record_id}.mp3'
    output_path = MP3_UPLOADED_FILES + new_full_name
    await convert_file_async(input_path, output_path)
    record = Record(id=record_id, file_name=new_full_name, orig_file_name=f"{filename}{ext}", owner=user)
    session.add(record)
    session.commit()
    return {"url": f"http://{HOST}:{PORT}/record?id={record_id}&user={user.id}"}


@router.get("/record", tags=["Download record"])
async def get_record(
        id: str,
        user: int,
        session: Session = Depends(get_db)):
    record = session.query(Record).filter_by(id=id, user_id=user).first()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found."
        )
    if not os.path.exists(MP3_UPLOADED_FILES + record.file_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found."
        )
    return FileResponse(
        MP3_UPLOADED_FILES + record.file_name,
        media_type="audio/mpeg",
        filename=record.file_name
    )
