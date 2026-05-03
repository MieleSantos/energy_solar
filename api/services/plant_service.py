from api import db
from api.exceptions import NotFoundError
from api.models import Plant
from api.schemas import plant_schema


def list_plants() -> list[Plant]:
    return Plant.query.order_by(Plant.id.desc()).all()


def create_plant(payload: dict) -> Plant:
    plant = plant_schema.load(payload)
    db.session.add(plant)
    db.session.commit()
    return plant


def delete_plant(plant_id: int) -> None:
    plant = db.session.get(Plant, plant_id)
    if plant is None:
        raise NotFoundError("Plant not found")

    db.session.delete(plant)
    db.session.commit()
