from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import config_dict
from api.errors import register_error_handlers

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_name: str = 'default') -> Flask:
    """App Factory pattern para criar instâncias do Flask de forma isolada."""
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    app.config.from_object(config_dict[config_name])

    # Inicializar extensões
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    from api import models  # noqa: F401

    # Registrar Blueprints
    from api.routes import bp as api_bp
    app.register_blueprint(api_bp)
    register_error_handlers(app)

    return app
