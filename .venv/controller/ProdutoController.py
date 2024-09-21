from flask import Blueprint, jsonify, request
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
            return "Erro ao listar produtos.", 500
    
    #findById
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
                # Retorna o produto como JSON
                return jsonify(produto), 200
            else:
                return 'Erro 404: produto não encontrado.', 404
        except Exception as e:
            print(f'Error: {e}')
            return 'Erro 500: erro interno do servidor.', 500
        
    @produto_bp.route('/produtos/categoria/<categoria>', methods = ['GET'])
    def find_by_category(categoria):
        try:
            categoria = str(categoria)
            produto = mongoConfig.produto_collection.find_one({'categoria':categoria})
            
            if produto:
                # Converte o ObjectId para string
                produto['_id'] = str(produto['_id'])
                # Retorna o produto como JSON
                return jsonify(produto), 200
            else:
                return 'Erro 404: produto não encontrado.', 404
            
        except Exception as e:
            print(f'Error: {e}')
            return 'Erro 500: erro interno do servidor.', 500
        
    #Cadastra produtos    
    @produto_bp.route("/inserirproduto", methods=['POST'])
    def set_produto():
        dados = request.get_json()
        
        novo_produto = Produto(
            id_produto=dados['id_produto'],
            nome=dados['nome'],
            descricao=dados['descricao'],
            valor_unitario=dados['valor_unitario'],
            categoria=dados["categoria"]
        )
        
        resultado = mongoConfig.produto_collection.insert_one(novo_produto.serialize())
        
        if  resultado.inserted_id:
            novo_produto.id_produto = str(resultado.inserted_id)
            return jsonify(novo_produto.serialize()), 201
        else:
            return "Erro ao inserir produto.", 500
        
    @produto_bp.route("/alteraproduto/<id_produto>", methods=["PUT"])
    def update_produto(id_produto):
        try:
            dados = request.get_json()

            # Converter id_produto para inteiro (ajuste se necessário)
            id_produto = int(id_produto)

            # Buscar o documento utilizando o id_produto personalizado
            resultado_busca = mongoConfig.produto_collection.find_one({"id_produto": id_produto})

            if resultado_busca:
                _id = resultado_busca["_id"]

                # Atualiza o documento utilizando o _id
                resultado_atualizacao = mongoConfig.produto_collection.update_one(
                    {"_id": _id},
                    {"$set": dados}
                )

                if resultado_atualizacao.modified_count == 1:
                    return f"produto {id_produto} atualizado com sucesso.", 200
                else:
                    return "Erro ao atualizar produto.", 500
            else:
                return f"produto com id {id_produto} não encontrado.", 404

        except Exception as e:
            return f"Erro ao atualizar produto: {e}", 500
        

    #exclui produto
    @produto_bp.route("/excluiproduto/<id_produto>", methods=["DELETE"])
    def delete_produto(id_produto):
        try:

            # Converter id_produto para inteiro (ajuste se necessário)
            id_produto = int(id_produto)

            # Buscar o documento utilizando o id_produto personalizado
            resultado_busca = mongoConfig.produto_collection.find_one({"id_produto": id_produto})

            if resultado_busca:
                _id = resultado_busca["_id"]

                resultado = mongoConfig.produto_collection.delete_one(
                    {"_id": _id}
                )
                print(resultado)
                if resultado.deleted_count == 1:
                    return f"produto {id_produto} excluido com sucesso.", 200
                else:
                    return f"produto com id {id_produto} não encontrado.", 404

        except Exception as e:
            return f"Erro ao excluir produto: {e}", 500

    # @produto_bp.route("/alteraProduto/<id_produto>", methods=["PUT"])
    # def update_produto(id_produto):
    #     try:
    #         dados = request.get_json()

    #         # Converter id_produto para inteiro (ajuste se necessário)
    #         id_produto = int(id_produto)

    #         # Buscar o documento utilizando o id_produto personalizado
    #         resultado_busca = mongoConfig.produto_collection.find_one({"id_produto": id_produto})

    #         if resultado_busca:
    #             _id = resultado_busca["_id"]

    #             # Atualiza o documento utilizando o _id
    #             resultado_atualizacao = mongoConfig.produto_collection.update_one(
    #                 {"_id": _id},
    #                 {"$set": dados}
    #             )

    #             if resultado_atualizacao.modified_count == 1:
    #                 return f"produto {id_produto} atualizado com sucesso.", 200
    #             else:
    #                 return f"Erro ao atualizar produto.", 500
    #         else:
    #             return f"produto com id {id_produto} não encontrado.", 404

    #     except Exception as e:
    #         return f"Erro ao atualizar produto: {e}", 500

