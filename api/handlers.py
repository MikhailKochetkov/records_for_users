import os
import ffmpeg
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import uuid4

from db.models import User, Record
from db.session import get_db
from .schemas import (
    UserCreateRequest,
    UserCreateResponse,
    RecordCreateResponse,
    RecordCreateRequest)
from settings import HOST, PORT, UPLOADED_FILES
from .file_handlers import (
    check_extension,
    format_filename)

router = APIRouter()


@router.post("/users", response_model=UserCreateResponse)
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


@router.post("/records", response_model=RecordCreateResponse)
async def create_record(request: RecordCreateRequest, session: Session = Depends(get_db)):
    user = session.query(User).filter_by(id=request.user_id, token=request.token).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user_id or token"
        )
    check_ext = check_extension(request.audio)
    if not check_ext:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File extension is not supported"
        )
    new_full_name = format_filename(request.audio)
    record_id = str(uuid4())
    input_path = fr"{request.audio}"
    output_path = UPLOADED_FILES + new_full_name
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


@router.get("/record")
async def get_record(file_id: str, user_id: int, session: Session = Depends(get_db)):
    record = session.query(Record).filter(file_id=file_id, user_id=user_id).first()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    if not os.path.exists(UPLOADED_FILES + record.file_name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    return FileResponse(
        UPLOADED_FILES + record.file_name,
        media_type="audio/mpeg",
        filename=record.file_name
    )
