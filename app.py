from data import *
from defaults import URI, DB_NAME, COLLECTION
import matplotlib.pyplot as plt
import io


class Project():
    def __init__(self, uri = URI, dbName = DB_NAME, collection = COLLECTION):
        self.db = connectToDb(uri, dbName)
        self.data = readToDataFrame(self.db, collection)
    
    def getData(self):
        return self.data

    def find(self, collection = COLLECTION, filter = {}, projection = None,\
         skip = 0, limit = 0, sort = None):
        try:
            result = self.db[collection].find(filter= filter, \
                projection= projection, skip= skip, limit= limit, sort= sort)
            return result
        except Exception as e:
            return str(e)

    def updateOne(self, collection = COLLECTION, filter = {}, update = None, upsert = False):
        try:
            assert update != None, "No update modifications passed"
            result = self.db[collection].update_one(filter= filter, update= update, upsert= upsert)
            return result
        except Exception as e:
            return str(e)
    
    def updateMany(self, collection = COLLECTION, filter = {}, update = None, upsert = False):
        try:
            assert update != None, "No update modifications passed"
            result = self.db[collection].update_many(filter= filter, update= update, upsert= upsert)
            return result
        except Exception as e:
            return str(e)

    def insertOne(self, collection = COLLECTION, data = None):
        try:
            assert data != None, "No data passed"
            result = self.db[collection].insert_one(data)
            return result
        except Exception as e:
            return str(e)

    def insertMany(self, collection = COLLECTION, data = None):
        try:
            assert data != None, "No data passed"
            result = self.db[collection].insert_many(data)
            return result
        except Exception as e:
            return str(e)

    def deleteOne(self, collection = COLLECTION, filter = None):
        try:
            assert filter != None, "No filter passed"
            result = self.db[collection].delete_one(filter)
            return result
        except Exception as e:
            return str(e)
    
    def deleteMany(self, collection = COLLECTION, filter = None):
        try:
            assert filter != None, "No filter passed"
            result = self.db[collection].delete_many(filter)
            return result
        except Exception as e:
            return str(e)

    def plot(self):
        plt.figure()
        self.data.plot()
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return bytes_image

    def head(self):
        return (self.data.head().values)

if __name__ == '__main__':
    plt.close('all')
    p = Project()
    # print(p.insertOne())
    # print(p.insertOne(data="sdss"))
    # print(list(p.find(limit=3)))
    # print (p.head())
    # df = p.getData()
    # print(p.plot())