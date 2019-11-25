from pymongo import MongoClient
from pandas import DataFrame

_USERNAME = 'admin'
_PASSWORD = 'admin'
_DB_NAME = 'food'
_URI = "mongodb+srv://{0}:{1}@cluster0-dohcp.mongodb.net".format(_USERNAME, _PASSWORD)

def connectToDb(uri = _URI, dbName = _DB_NAME):
    client = MongoClient(uri)
    db = client[dbName]
    return db

def readToDataFrame(db, collection, query = {}, projection = {'_id': 0}):
    cursor = db[collection].find(query, projection= projection)
    df = DataFrame(list(cursor))
    return df