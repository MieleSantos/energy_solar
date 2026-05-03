from datetime import datetime, timezone
from api import db

class Plant(db.Model):
    __tablename__ = 'plants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False, default='Desconhecida')
    capacity_kw = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Ativa') # Ativa, Em Construção, Manutenção, Inativa
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
