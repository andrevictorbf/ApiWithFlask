
class Pedido():
   
    def __init__(self, produtos, id_cliente, data, valor_final, quantidade_itens):
        self.produtos = produtos
        self.id_cliente = id_cliente
        self.data = data
        self.valor_final = valor_final
        self.quantidade_itens = quantidade_itens
        
    def serialize(self):
        return {
            "produtos": self.produtos,
            "id_cliente": self.id_cliente,
            "data":self.data,
            "quantidade_itens": self.quantidade_itens,
            "valor_final": self.valor_final
        }

    