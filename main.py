import pickle
from pathlib import Path
from rich.console import Console
from fourierdb import FourierDocument, FourierCollection, FourierDB

console = Console()

doc = FourierDocument({"bar": "eggs", "xyz": "spam"})
doc2 = FourierDocument({"a": "foo", "b": "bar"})
doc3 = FourierDocument({"abc": "xyz"})
doc4 = FourierDocument({1: 2, 3: 4, 5: 6})
doc5 = FourierDocument({"hello": [1, 2, 3, 4, 5, 6, 7, 8, 9]})
FOURIER_DIR = Path.home() / ".fourier"
FOURIER_LOGS = FOURIER_DIR / "logs"
FOURIER_DBS = FOURIER_DIR / "databases"
coll = FourierCollection("coll", doc, doc2)
coll2 = FourierCollection("coll2", doc3, doc4, doc5)

db = FourierDB("db")

db.add_collection(coll)
db.add_collection(coll2)

pickle.dump(db, open(""))