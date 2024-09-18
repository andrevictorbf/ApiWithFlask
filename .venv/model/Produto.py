class Produto():
    
    def __init__(self, id, nome, descricao, valor_unitario, categoria):
        
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.valor_unitario = valor_unitario
        self.categoria = categoria
    
    def serialize(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "valor_unitario": self.valor_unitario,
            "categoria": self.categoria
        }

    