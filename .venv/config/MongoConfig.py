from pymongo import MongoClient

class MongoConfig:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['banco_flaskpy']
        self.pedido_collection = self.db['pedido']
        self.cliente_collection = self.db['cliente']
        self.produto_collection = self.db['produto']
