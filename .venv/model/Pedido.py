class Pedido():
   
    def __init__(self, id_produto, id_cliente, data, valor_final):
        self.id_produto = id_produto
        self.id_cliente = id_cliente
        self.data = data
        self.valor = valor_final
    
    def serialize(self):
        return {
            "id_produto": self.id_produto,
            "id_cliente": self.id_cliente,
            
        }

    