from http import HTTPStatus
from pathlib import Path

FOURIER_DIR = Path.home() / ".fourier"
FOURIER_LOGS = FOURIER_DIR / "logs"
FOURIER_DBS = FOURIER_DIR / "databases"
FOURIER_CACHE = FOURIER_DIR / ".cache.json"


def get_databases():
    if not (Path.home() / ".fourier").exists():
        return []
    databases = [f.stem for f in (Path.home() / ".fourier" / "databases").glob("*.db")]
    return databases


def get_db_file(database_name: str) -> Path:
    return Path(FOURIER_DBS / f"{database_name}.db")


def get_status_message(status_code: int) -> str:
    return HTTPStatus(status_code).phrase
