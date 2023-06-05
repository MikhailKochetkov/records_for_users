from fastapi import FastAPI, APIRouter
from api.handlers import router


application = FastAPI(title="Create users and save audio records")
main_router = APIRouter()

main_router.include_router(router)
application.include_router(main_router)
