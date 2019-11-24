from data import *
import matplotlib.pyplot as plt
import io


_USERNAME = 'admin'
_PASSWORD = 'admin'
_DB_NAME = 'food'
_COLLECTION = 'FAO'
_URI = "mongodb+srv://{0}:{1}@cluster0-dohcp.mongodb.net".format(_USERNAME, _PASSWORD)

class Project():
    def __init__(self, uri = _URI, dbName = _DB_NAME, collection = _COLLECTION):
        self.db = connectToDb(uri, dbName)
        self.data = readToDataFrame(self.db, collection)
    
    def getData(self):
        return self.data

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
    print (p.head())
    df = p.getData()
    print(p.plot())