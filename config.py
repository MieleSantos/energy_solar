import os
import secrets

class Config:
    """Configuração base do projeto."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Gera chave efêmera para dev/local quando não definida no ambiente.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

class DevelopmentConfig(Config):
    """Configuração de Desenvolvimento."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///local.db')

class TestingConfig(Config):
    """Configuração de Testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Banco em memória para testes rápidos

config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
