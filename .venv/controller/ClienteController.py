from flask import Flask, app, jsonify, request, Blueprint
from config.MongoConfig import MongoConfig  
from model.Cliente import Cliente
from bson import ObjectId
from pymongo.errors import NetworkTimeout, ServerSelectionTimeoutError, OperationFailure
from bson.errors import InvalidId


cliente_bp = Blueprint('cliente_bp', __name__)
mongoConfig = MongoConfig() #instancia a classe de configuracao
class ClienteController:
    
    #Find All - todos os clientes
    @cliente_bp.route('/clientes', methods=['GET'])
    def find_all():
        try:
            # Tenta buscar todos os clientes na coleção
            clientes = mongoConfig.cliente_collection.find()

            # Serializa os documentos, convertendo ObjectId para string
            clientes_serializado = [
                {**cliente, '_id': str(cliente['_id'])} for cliente in clientes
            ]

            # Retorna a lista de clientes serializados
            return jsonify(clientes_serializado), 200

        except NetworkTimeout:
            # timeout de conexão com o MongoDB
            return 'Erro 500: Tempo de conexão com o banco de dados esgotado.', 500

        except ServerSelectionTimeoutError:
            # timeout
            return 'Erro 500: Não foi possível conectar ao servidor MongoDB.', 500

        except OperationFailure:
            # erro de operação do MongoDB
            return 'Erro 500: Falha ao executar a operação no MongoDB.', 500

        except InvalidId:
            #  erros relacionados a ObjectId inválido
            return 'Erro 400: ObjectId inválido.', 400

        except ValueError as ve:
            # captura erros de valor
            print(f'Error: {ve}')
            return 'Erro 400: Um valor inválido foi fornecido.', 400

        except Exception as e:
            #exceções gerais
            print(f'Error: {e}')
            return 'Erro 500: Erro ao listar clientes.', 500

    #Find By id_cliente 
    @cliente_bp.route('/clientes/<id_cliente>', methods=['GET'])
    def find_by_id(id_cliente):
        try:
            # converte para int
            id_cliente = int(id_cliente)
            # Busca o cliente pelo id na coleção do MongoDB
            cliente = mongoConfig.cliente_collection.find_one({'id_cliente': id_cliente})
            
            if cliente:
                # Converte o ObjectId para string
                cliente['_id'] = str(cliente['_id'])
                # Retorna o cliente como JSON
                return jsonify(cliente), 200
            else:
                return 'Erro 404: cliente não encontrado.', 404
        except ValueError:
            return 'Erro: id_cliente deve ser um número inteiro.', 400
        except Exception as e:
            print(f'Error: {e}')
            return 'Erro 500: erro interno do servidor.', 500
        
    

#cadastra clientes
    @cliente_bp.route("/inserirCliente", methods=['POST'])
    def set_cliente():
        try:
            # Pega dados da requisicao
            dados = request.get_json()

            # Cria um novo objeto Cliente com os dados fornecidos
            novo_cliente = Cliente(
                id_cliente=dados['id_cliente'],
                nome=dados['nome'],
                email=dados['email'],
                cpf=dados['cpf'],
                data_nascimento=dados['data_nascimento']
            )

            # Insere o cliente no banco de dados MongoDB
            resultado = mongoConfig.cliente_collection.insert_one(novo_cliente.serialize())

            # Verifica se o cliente foi inserido corretamente
            if resultado.inserted_id:
                novo_cliente.id_cliente = str(resultado.inserted_id)  # Converte o ObjectId para string
                return jsonify(novo_cliente.serialize()), 201
            else:
                return "Erro ao inserir cliente.", 500

        except KeyError as e:
            # Trata o caso de algum campo obrigatório estar faltando
            return f"Erro 400: Campo obrigatório ausente: {str(e)}", 400

        except Exception as e:
            # Captura qualquer outro erro e imprime para depuração
            print(f"Erro: {e}")
            return "Erro 500: Erro interno do servidor.", 500
        
        
    #metodo de atualizacao do cliente   
    @cliente_bp.route("/alterarCliente/<id_cliente>", methods=["PUT"])
    def update_cliente(id_cliente):
        try:
            dados = request.get_json()

            # Converter id_cliente para inteiro (ajuste se necessário)
            id_cliente = int(id_cliente)

            # Buscar o documento utilizando o id_cliente personalizado
            resultado_busca = mongoConfig.cliente_collection.find_one({"id_cliente": id_cliente})

            if resultado_busca:
                _id = resultado_busca["_id"]

                # Atualiza o documento utilizando o _id
                resultado_atualizacao = mongoConfig.cliente_collection.update_one(
                    {"_id": _id},
                    {"$set": dados}
                )

                if resultado_atualizacao.modified_count == 1:
                    return f"Cliente {id_cliente} atualizado com sucesso.", 200
                else:
                    return "Erro ao atualizar cliente.", 500
            else:
                return f"Cliente com id {id_cliente} não encontrado.", 404

        except Exception as e:
            return f"Erro ao atualizar cliente: {e}", 500
        
    #metodo de exclusao do cliente
    @cliente_bp.route("/excluirCliente/<id_cliente>", methods=["DELETE"])
    def delete_cliente(id_cliente):
        try:

            # Converter id_cliente para inteiro (ajuste se necessário)
            id_cliente = int(id_cliente)

            # Buscar o documento utilizando o id_cliente personalizado
            resultado_busca = mongoConfig.cliente_collection.find_one({"id_cliente": id_cliente})

            if resultado_busca:
                _id = resultado_busca["_id"]

                resultado = mongoConfig.cliente_collection.delete_one(
                    {"_id": _id}
                )

                if resultado.deleted_count == 1:
                    return f"Cliente {id_cliente} excluido com sucesso.", 200
                else:
                    return f"Cliente com id {id_cliente} não encontrado.", 404
        except Exception as e:
            return f"Erro ao excluir cliente: {e}", 500
        
    
        
        



