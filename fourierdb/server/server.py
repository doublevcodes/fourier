import uvicorn
from pathlib import Path
from fourierdb import FourierDB
from fastapi import FastAPI

server = FastAPI()

FOURIER_DIR = Path.home() / ".fourier"
FOURIER_LOGS = FOURIER_DIR / "logs"
FOURIER_DBS = FOURIER_DIR / "databases"


@server.on_event("startup")
async def start_server():
    FOURIER_DIR.mkdir(exist_ok=True)
    FOURIER_LOGS.mkdir(exist_ok=True)
    FOURIER_DBS.mkdir(exist_ok=True)


@server.post("/")
async def create_db(name: str):
    new_db = FourierDB(name)

@server.get("/")
async def return_root():
    return {"message": "Hi"}

def run_server(port):
    uvicorn.run(server, port=port)

if __name__ == "__main__":
    run_server(8080)