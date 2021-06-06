import time


def construct_snowflake() -> int:
    milliseconds_from_epoch: int = time.time_ns() // 1_000_000
    process_time: int = time.process_time_ns()
    concat_times: int = int(str(milliseconds_from_epoch) + str(process_time))
    snowflake: int = concat_times >> 4
    return snowflake


class FourierDocument(dict):
    def __init__(self, data: dict = {}) -> None:
        data["_id"] = construct_snowflake()
        return super().__init__(data)


class FourierCollection(dict):
    def __init__(self, name: str, *documents):
        self.name = name
        return super().__init__({doc["_id"]: doc for doc in documents})

    def insert(self, document: FourierDocument):
        self[document["_id"]] = document


class FourierDB(dict):
    def __init__(self, name: str):
        self.name = name
        return super().__init__()

    def add_collection(self, collection: FourierCollection):
        self[collection.name] = collection
