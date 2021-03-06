import json
import os
import pickle
from typing import Any, Union
from pathlib import Path

from uvicorn import run
from fourierdb import FourierDB, FourierCollection, FourierDocument
from fastapi import FastAPI, Request, Response, status

from fourierdb.helpers import get_databases, get_db_file, get_status_message


server: FastAPI = FastAPI()

FOURIER_DIR: Path = Path.home() / ".fourier"
FOURIER_LOGS: Path = FOURIER_DIR / "logs"
FOURIER_DBS: Path = FOURIER_DIR / "databases"
FOURIER_CACHE: Path = FOURIER_DIR / ".cache.json"


@server.on_event("startup")
async def start_server():
    FOURIER_DIR.mkdir(exist_ok=True)
    FOURIER_LOGS.mkdir(exist_ok=True)
    FOURIER_DBS.mkdir(exist_ok=True)


@server.head("/")
async def root() -> None:
    """
    Use to check server connection
    """
    return dict()


@server.get("/")
async def get_dbs(response: Response) -> dict[str, Union[str, list[str]]]:
    """
    Return an array of current database names
    """

    databases: list[str] = get_databases()

    response.status_code = status.HTTP_200_OK
    return {"message": get_status_message(response.status_code), "databases": databases}


@server.get("/{database_name}")
async def get_db(
    database_name: str, response: Response
) -> Union[dict[str, str], dict[str, dict[str, dict[Any, Any]]]]:
    """
    Return a dictionary representing the database requested.
    """

    db_file: Path = get_db_file(database_name)

    if not db_file.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": database_name,
        }

    db: FourierDB = pickle.load(open(db_file, "rb"))

    response.status_code = status.HTTP_200_OK
    return dict(db)


@server.post("/{database_name}")
async def create_db(database_name: str, response: Response) -> dict[str, str]:
    """
    Create a new database with the requested name.
    """

    new_db: FourierDB = FourierDB(database_name)
    new_db_file: Path = get_db_file(database_name)

    if new_db_file.exists():
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {
            "message": get_status_message(response.status_code),
            "name": database_name,
        }

    with open(new_db_file, "wb+") as db_file:
        pickle.dump(new_db, db_file)

    response.status_code = status.HTTP_201_CREATED
    return {"message": get_status_message(response.status_code), "name": database_name}


@server.delete("/{database_name}")
async def remove_db(database_name: str, response: Response) -> dict[str, str]:
    """
    Delete the database with the requested name.
    """

    db_file: Path = get_db_file(database_name)

    if not db_file.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": database_name,
        }

    # Set `missing_ok` to `False` because we want an internal server error if the database
    # does not exist but the previous if statement failed
    db_file.unlink(missing_ok=False)

    response.status_code = status.HTTP_200_OK
    return {"message": get_status_message(response.status_code), "name": database_name}


@server.get("/{database_name}/{collection_name}")
async def get_collection(
    database_name: str, collection_name, response: Response
) -> Union[dict[str, str], dict[str, dict[Any, Any]]]:
    """
    Get a collection from the requested database with the requested name.
    """

    db_file: Path = get_db_file(database_name)

    if not db_file.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": database_name,
        }

    db: FourierDB = pickle.load(open(db_file, "rb"))
    collection: FourierCollection = db.get(collection_name, False)

    if not collection:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": collection_name,
        }

    response.status_code = status.HTTP_200_OK
    return dict(collection)


@server.post("/{database_name}/{collection_name}")
async def insert_collection(
    database_name: str, collection_name: str, response: Response
) -> dict[str, str]:
    """
    Create a new collection in the requested database with the requested name.
    """

    db_file: Path = get_db_file(database_name)

    if not db_file.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": database_name,
        }

    db: FourierDB = pickle.load(open(db_file, "rb"))
    collection = db.get(collection_name, False)

    if collection:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            "message": get_status_message(response.status_code),
            "name": collection_name,
        }

    new_collection: FourierCollection = FourierCollection(collection_name)

    db.add_collection(new_collection)
    pickle.dump(db, open(db_file, "wb"))

    response.status_code = status.HTTP_201_CREATED
    return {
        "message": get_status_message(response.status_code),
        "name": collection_name,
    }


@server.delete("/{database_name}/{collection_name}")
async def remove_collection(
    database_name: str, collection_name: str, response: Response
) -> dict[str, str]:
    """
    Delete the collection from the requested database with the requested name.
    """

    db_file: Path = get_db_file(database_name)

    if not db_file.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": database_name,
        }

    db: FourierDB = pickle.load(open(db_file, "rb"))
    collection: FourierCollection = db.get(collection_name, False)

    if not collection:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": collection_name,
        }

    pickle.dump(db, open(db_file, "wb"))

    response.status_code = status.HTTP_200_OK
    return {
        "message": get_status_message(response.status_code),
        "name": collection_name,
    }


@server.post("/{database_name}/{collection_name}/documents")
async def insert_document(
    request: Request, database_name: str, collection_name: str, response: Response
) -> Union[dict[str, str], dict[str, Union[str, dict[Any, Any]]]]:
    """
    Insert the request's body as a document into the requested collection from the requested datbase.
    """

    db_file = get_db_file(database_name)

    if not db_file.exists():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": database_name,
        }

    db: FourierDB = pickle.load(open(db_file, "rb"))
    collection: FourierCollection = db.get(collection_name, False)

    if not collection:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "message": get_status_message(response.status_code),
            "name": collection_name,
        }

    request_body = await request.json()
    document = FourierDocument(request_body)

    collection.insert(document)
    pickle.dump(db, open(db_file, "wb"))

    response.status_code = status.HTTP_200_OK
    return {
        "message": get_status_message(response.status_code),
        "document": dict(document),
    }


@server.on_event("shutdown")
async def server_stop() -> None:
    with open(FOURIER_CACHE, "w") as cache:
        json.dump({"server": False}, cache)


def run_server(port) -> None:
    Path.home().mkdir(exist_ok=True, parents=True)
    FOURIER_DIR.mkdir(exist_ok=True)
    FOURIER_CACHE.touch(exist_ok=True)
    with open(FOURIER_CACHE, "w") as cache:
        json.dump({"server": True, "port": port}, cache)
    run(server, port=port)


if __name__ == "__main__":
    run_server(2359)
