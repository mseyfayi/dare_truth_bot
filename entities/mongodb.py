from typing import List, Optional, Dict

import pymongo
from decouple import config

environment = config("ENV")

is_development = environment == 'development'

if is_development:
    con_str = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(con_str)
    db = client["dare_truth"]
else:
    cluster = config("MONGO_CLUSTER")
    db_name = config("MONGO_DBNAME")
    db_pass = config("MONGO_PASS")
    db_user = config("MONGO_USER")

    con_str = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(db_user, db_pass, cluster, db_name)
    client = pymongo.MongoClient(con_str)
    db = client.get_database("dare_truth")


def get_collection(collection_name):
    if is_development:
        collection = db[collection_name]
    else:
        collection = db.get_collection(collection_name)
    return collection


def mdb_insert(collection_name: str, data: Dict[str, str]) -> str:
    collection = get_collection(collection_name)
    print("inserting: ", collection_name, data)
    x = collection.insert_one(data)
    return str(x.inserted_id)


def mdb_update(collection_name: str, new_data: Dict[str, any], query: Dict[str, any]):
    collection = get_collection(collection_name)
    new_data = {"$set": new_data}
    print("updating: ", collection_name, new_data, query)
    collection.update_one(query, new_data)


def mdb_select(collection_name: str, query: Optional[Dict[str, any]] = None) -> List[Dict[str, any]]:
    collection = get_collection(collection_name)
    return [x for x in collection.find(query)]


def mdb_delete(collection_name: str, query: Dict[str, any]) -> None:
    collection = get_collection(collection_name)
    print("deleting: ", collection_name, query)
    collection.delete_many(query)
