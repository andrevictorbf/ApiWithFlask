from flask import Flask
from controller import ClienteController
from controller import ProdutoController
from controller import PedidoController

def create_app():
    app = Flask(__name__)
    
    # Registrar o blueprint
    app.register_blueprint(ClienteController.cliente_bp)
    app.register_blueprint(ProdutoController.produto_bp)
    app.register_blueprint(PedidoController.pedido_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()  
    app.run(debug=True)  # Roda o servidor com a aplicação Flask
