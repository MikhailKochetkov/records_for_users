import uvicorn
from fastapi import FastAPI, APIRouter
from api.handlers import router

from settings import HOST, PORT


application = FastAPI()
main_router = APIRouter()

main_router.include_router(router)
application.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(application, host=HOST, port=int(PORT))
