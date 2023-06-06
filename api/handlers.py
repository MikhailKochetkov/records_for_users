import os
import ffmpeg
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    UploadFile,
    File)
from fastapi.responses import FileResponse
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
    UPLOADED_FILES,
    WAV_UPLOADED_FILES,
    MP3_UPLOADED_FILES)
from .file_handlers import (
    check_extension,
    format_filename,
    save_file_to_uploads,
    new_format_filename)

router = APIRouter()


@router.post("/users", tags=["Create user"], response_model=UserCreateResponse)
async def create_user(
        request: UserCreateRequest,
        session: Session = Depends(get_db)):
    if session.query(User).filter_by(email=request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User email already exists"
        )
    user = User(
        name=request.name,
        token=str(uuid4()),
        email=request.email
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
    user = session.query(User).filter_by(id=user_id, token=token).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user_id or token"
        )
    if not check_extension(file):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File extension is not supported"
        )
    if not os.path.exists(UPLOADED_FILES):
        os.mkdir(UPLOADED_FILES)
    if not os.path.exists(MP3_UPLOADED_FILES):
        os.mkdir(MP3_UPLOADED_FILES)
    if not os.path.exists(WAV_UPLOADED_FILES):
        os.mkdir(WAV_UPLOADED_FILES)
    full_name = format_filename(file)
    await save_file_to_uploads(file, full_name)
    old_filepath = WAV_UPLOADED_FILES + full_name
    new_full_name = new_format_filename(old_filepath)
    record_id = str(uuid4())
    input_path = fr"{old_filepath}"
    output_path = MP3_UPLOADED_FILES + new_full_name
    if os.path.exists(output_path):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="File already exists"
        )
    with open(input_path, "rb") as f:
        f.read()
    try:
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path)
        ffmpeg.run(stream)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    record = Record(file_id=record_id, file_name=new_full_name, owner=user)
    session.add(record)
    session.commit()
    return {"url": f"http://{HOST}:{PORT}/record?id={record_id}&user={user.id}"}


@router.get("/record", tags=["Download record"])
async def get_record(
        id: str,
        user: int,
        session: Session = Depends(get_db)):
    record = session.query(Record).filter_by(file_id=id, user_id=user).first()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    if not os.path.exists(MP3_UPLOADED_FILES + record.file_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    return FileResponse(
        MP3_UPLOADED_FILES + record.file_name,
        media_type="audio/mpeg",
        filename=record.file_name
    )
