from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import config_dict

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name: str = 'default') -> Flask:
    """App Factory pattern para criar instâncias do Flask de forma isolada."""
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    app.config.from_object(config_dict[config_name])

    # Inicializar extensões
    db.init_app(app)
    ma.init_app(app)

    # Registrar Blueprints
    from api.routes import bp as api_bp
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
