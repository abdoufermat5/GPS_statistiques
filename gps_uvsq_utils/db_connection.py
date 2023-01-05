from pymongo import MongoClient


class DBConnection:

    def __init__(self):
        self.client = MongoClient('mongodb+srv://cluster0.nkdni.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['DonneeGPS']
        self.collection = self.db['DATAGPS']

    def get_collection(self):
        return self.collection

    def get_db(self):
        return self.db
