import pytest
from api import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_plant(client):
    response = client.post('/api/plants', json={
        'name': 'Usina Teste',
        'location': 'Rio de Janeiro',
        'capacity_kw': 1500.0,
        'status': 'Ativa'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Usina Teste'
    assert data['capacity_kw'] == 1500.0

def test_create_plant_validation_error(client):
    response = client.post('/api/plants', json={
        'name': '', # Validation error: min length 1
        'capacity_kw': -10 # Validation error: min 0.1
    })
    assert response.status_code == 422
    data = response.get_json()
    assert "details" in data


def test_create_plant_without_payload(client):
    response = client.post("/api/plants", json=None)
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "No input data provided"

def test_get_plants(client):
    # Setup test data
    client.post('/api/plants', json={
        'name': 'Usina Alpha',
        'capacity_kw': 500
    })
    
    response = client.get('/api/plants')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Usina Alpha'

def test_delete_plant(client):
    post_res = client.post('/api/plants', json={
        'name': 'Usina Beta',
        'capacity_kw': 200
    })
    plant_id = post_res.get_json()['id']
    
    del_res = client.delete(f'/api/plants/{plant_id}')
    assert del_res.status_code == 200
    
    get_res = client.get('/api/plants')
    assert len(get_res.get_json()) == 0


def test_delete_plant_not_found(client):
    response = client.delete("/api/plants/99999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Plant not found"
