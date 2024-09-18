from flask import Blueprint, jsonify
from config.MongoConfig import MongoConfig  
from model.Produto import Produto

produto_bp = Blueprint('produto_bp', __name__)
mongoConfig = MongoConfig() #instancia a classe de config

class ProdutoController:
    #metodos get de produto
    # metodo findAll - lista todos os produtos cadastrados
    @produto_bp.route('/produtos', methods = ['GET'])
    def find_all():
        try:
            produtos = mongoConfig.produto_collection.find()
            produtos_serializado = []
            for produto in produtos:
                produto['_id'] = str(produto['_id'])
                produtos_serializado.append(produto)
            return jsonify(produtos_serializado), 200
        
        except Exception as e:
            print(f"Erro: {e}")
            return "Erro ao listar clientes.", 500
        
    @produto_bp.route('/produtos/<id_produto>', methods = ['GET'])
    def find_by_id(id_produto):
        try:
            #converte para int
            id_produto = int(id_produto)
            #metodo de busca no banco  - find_one
            produto = mongoConfig.produto_collection.find_one({'id_produto':id_produto})
            
            if produto:
                # Converte o ObjectId para string
                produto['_id'] = str(produto['_id'])
                # Retorna o cliente como JSON
                return jsonify(produto), 200
            else:
                return 'Erro 404: cliente não encontrado.', 404
            
        except Exception as e:
            raise e
        
    
