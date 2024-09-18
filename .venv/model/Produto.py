class Produto():
    def __init__(self, id_produto, nome, descricao, valor_unitario, categoria):
        
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.valor_unitario = valor_unitario
        self.categoria = categoria
    
    def serialize(self):
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "valor_unitario": self.valor_unitario,
            "categoria": self.categoria
        }

    