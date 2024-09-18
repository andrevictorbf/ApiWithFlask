
class Cliente():
    def __init__(self, id_cliente, nome, email, cpf, data_nascimento):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimento
    
    def serialize(self): 
        return {
            "id_cliente": self.id_cliente, 
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento
        }
        


    