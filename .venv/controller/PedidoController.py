from flask import request, jsonify, Blueprint 
from model.Pedido import Pedido
from config.MongoConfig import MongoConfig  
from bson import ObjectId


pedido_bp = Blueprint('pedido_bp', __name__) 
mongoConfig = MongoConfig() 

class PedidoController:
    #criacao do pedido
    @pedido_bp.route("/pedidos", methods=['GET'])
    def find_all():
        try:
            pedidos = mongoConfig.pedido_collection.find()
            pedido_serializado = [
                {**pedido, '_id': str(pedido['_id'])} for pedido in pedidos
            ]
            return jsonify(pedido_serializado), 200
        except Exception as e:
            print(f'Error: {e}')
            return 'Erro 500: Erro ao listar pedidos.', 500
    
    #find by ObjectId do banco de dados mongo
    @pedido_bp.route("/pedidos/<_id>", methods = ['GET'])
    def get_by_obj_id(_id):
        try:
            pedido = mongoConfig.pedido_collection.find_one({'_id': ObjectId(_id)})
            if pedido:
                pedido['_id'] = str(pedido['_id'])
                return jsonify(pedido), 200
            else:
                return jsonify({'message': 'Pedido nao encontrado'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        
#Cadastro de novo pedido  - permitindo criar um array de produtos
@pedido_bp.route("/pedidos", methods=['POST'])
def set_pedido():
    dados = request.get_json()
    id_cliente = dados.get('id_cliente')
    produtos = dados.get('produtos')

    # Verificar se 'produtos' não é None
    if not produtos:
        return jsonify({"error": "Lista de produtos não fornecida ou está vazia"}), 400

    # Verificar se o cliente existe
    cliente = mongoConfig.cliente_collection.find_one({"id_cliente": id_cliente})
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    # Verificar se cada produto existe
    for produto in produtos:
        id_produto = produto.get('id_produto')  
        if not id_produto:
            return jsonify({"error": "Produto inválido"}), 400

        produto_existente = mongoConfig.produto_collection.find_one({"id_produto": id_produto})
        if not produto_existente:
            return jsonify({"error": f"Produto id {id_produto} não encontrado"}), 404

    # Criar o novo pedido
    novo_pedido = Pedido(
        id_cliente=id_cliente,
        produtos=produtos,
        data=dados.get('data'),
        quantidade_itens=dados.get('quantidade_itens'),
        valor_final=dados.get('valor_final')
    )

    resultado = mongoConfig.pedido_collection.insert_one(novo_pedido.serialize())
    if resultado.inserted_id:
        return jsonify(novo_pedido.serialize(), "Pedido realizado com sucesso."), 201
    else:
        return jsonify({"Erro ao criar pedido"}), 500
    
    
    






