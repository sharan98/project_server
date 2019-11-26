_USERNAME = 'admin'
_PASSWORD = 'admin'
DB_NAME = 'food'
COLLECTION = 'FAO'
URI = "mongodb+srv://{0}:{1}@cluster0-dohcp.mongodb.net".format(_USERNAME, _PASSWORD)

findArgsJSON = {
    'collection': COLLECTION,
    'filter': {},
    'projection': {'_id':0},
    'skip': 0,
    'limit': 0,
    'sort': None
}

updateArgsJSON = {
    'collection': COLLECTION,
    'filter': {},
    'update': None,
    'upsert': False
}

insertArgsJSON = {
    'collection': COLLECTION,
    'data': None
}

deleteArgsJSON = {
    'collection': COLLECTION,
    'filter': None
}