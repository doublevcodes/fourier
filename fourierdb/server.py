import uvicorn
import pickle
from pathlib import Path
from fourierdb import FourierDB, FourierCollection, FourierDocument
from fastapi import FastAPI, Request, Response

server = FastAPI()

FOURIER_DIR = Path.home() / ".fourier"
FOURIER_LOGS = FOURIER_DIR / "logs"
FOURIER_DBS = FOURIER_DIR / "databases"


@server.on_event("startup")
async def start_server():
    FOURIER_DIR.mkdir(exist_ok=True)
    FOURIER_LOGS.mkdir(exist_ok=True)
    FOURIER_DBS.mkdir(exist_ok=True)

@server.get("/{database_name}", status_code=200)
async def get_db(database_name: str, response: Response):
    db_file = Path(FOURIER_DBS / f"{database_name}.db")
    if not(db_file.exists()):
        response.status_code = 404
        return {"message": f"The database {database_name} was not found"}
    db = pickle.load(open(db_file, "rb"))
    return dict(db)

@server.post("/{database_name}", status_code=201)
async def create_db(database_name: str, response: Response):
    new_db = FourierDB(database_name)
    new_db_file = Path(FOURIER_DBS / f"{database_name}.db")
    if new_db_file.exists():
        response.status_code = 409
        return {"message": "Resource already exists"}
    with open(new_db_file, "wb+") as db_file:
        pickle.dump(new_db, db_file)
    return {"message": "Database created", "name": database_name}

@server.delete("/{database_name}", status_code=200)
async def remove_db(database_name: str, response: Response):
    db_file = Path(FOURIER_DBS / f"{database_name}.db")
    if not(db_file.exists()):
        response.status_code = 404
        return {"message": f"The database {database_name} was not found"}
    db_file.unlink(missing_ok=False)
    return {"message": f"The database {database_name} was successfully deleted"}

@server.get("/{database_name}/{collection_name}", status_code=200)
async def get_collection(database_name: str, collection_name, response: Response):
    db_file = Path(FOURIER_DBS / f"{database_name}.db")
    db: FourierDB = pickle.load(open(db_file, "rb"))
    collection = db[collection_name]
    return dict(collection)

@server.post("/{database_name}/{collection_name}", status_code=201)
async def insert_collection(database_name: str, collection_name: str):
    db_file = Path(FOURIER_DBS / f"{database_name}.db")
    db: FourierDB = pickle.load(open(db_file, "rb"))
    new_collection = FourierCollection(collection_name)
    db.add_collection(new_collection)
    pickle.dump(db, open(db_file, "wb"))
    return {"message": "Collection added successfully", "name": collection_name}

@server.delete("/{database_name}/{collection_name}", status_code=200)
async def remove_collection(database_name: str, collection_name: str, response: Response):
    db_file = Path(FOURIER_DBS / f"{database_name}.db")
    db: FourierDB = pickle.load(open(db_file, "rb"))
    db.remove_collection(collection_name)
    pickle.dump(db, open(db_file, "wb"))
    return {"message": f"The collection {collection_name} was successfully deleted"}

@server.post("/{database_name}/{collection_name}/documents", status_code=201)
async def insert_document(request: Request, database_name: str, collection_name: str, response: Response):
    db_file = Path(FOURIER_DBS / f"{database_name}.db")
    db: FourierDB = pickle.load(open(db_file, "rb"))
    coll: FourierCollection = db.get(collection_name)
    coll.insert(FourierDocument(await request.json()))
    pickle.dump(db, open(db_file, "wb"))
    return {"message":"Created document"}

def run_server(port):
    uvicorn.run(server, port=port)

if __name__ == "__main__":
    run_server(2359)