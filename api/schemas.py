from api import ma
from api.models import Plant
from marshmallow import fields, validate

class PlantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Plant
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True, validate=validate.Length(min=1, max=100))
    location = ma.auto_field()
    capacity_kw = ma.auto_field(required=True, validate=validate.Range(min=0.1))
    status = fields.String(validate=validate.OneOf(['Ativa', 'Em Construção', 'Manutenção', 'Inativa']))
    created_at = ma.auto_field(dump_only=True)

plant_schema = PlantSchema()
plants_schema = PlantSchema(many=True)
