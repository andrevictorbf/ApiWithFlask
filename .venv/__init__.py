from flask import Flask
from controller import ClienteController

def create_app():
    app = Flask(__name__)
    
    # Registrar o blueprint
    app.register_blueprint(ClienteController.cliente_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()  # Cria a instância do Flask a partir de create_app()
    app.run(debug=True)  # Roda o servidor com a aplicação Flask
