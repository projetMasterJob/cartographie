import pytest
from app import create_app, db
from models.company import Company
from models.job import Job
from models.location import Location
import uuid

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_map_entities_missing_params(client):
    response = client.get('/map/entities')
    assert response.status_code == 400
    assert 'center_lat' in response.json['error']
    response = client.get('/map/entities?center_lat=48.85')
    assert response.status_code == 400
    assert 'center_lat' in response.json['error']

def test_get_map_entities_valid_params_empty(client):
    response = client.get('/map/entities?center_lat=48.85&center_lng=2.35')
    assert response.status_code == 200
    assert "companies" in response.json
    assert "jobs" in response.json
    assert response.json["companies"] == []
    assert response.json["jobs"] == []

def test_get_map_entities_with_company_in_zone(client):
    company = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="MapCompany",
        description="desc",
        website="https://test.com"
    )
    location = Location(
        entity_type='company',
        entity_id=company.id,
        latitude=48.85,
        longitude=2.35,
        address="Paris",
        cp="75000"
    )
    with client.application.app_context():
        db.session.add(company)
        db.session.add(location)
        db.session.commit()
    response = client.get('/map/entities?center_lat=48.85&center_lng=2.35&radius_km=1')
    assert response.status_code == 200
    assert len(response.json["companies"]) == 1
    assert response.json["companies"][0]["name"] == "MapCompany"

def test_get_map_entities_with_job_in_zone(client):
    job = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="MapJob",
        description="desc job",
        salary=10000,
        job_type="full_time"
    )
    location = Location(
        entity_type='job',
        entity_id=job.id,
        latitude=48.85,
        longitude=2.35,
        address="Paris",
        cp="75000"
    )
    with client.application.app_context():
        db.session.add(job)
        db.session.add(location)
        db.session.commit()
    response = client.get('/map/entities?center_lat=48.85&center_lng=2.35&radius_km=1')
    assert response.status_code == 200
    assert len(response.json["jobs"]) == 1
    assert response.json["jobs"][0]["title"] == "MapJob"

def test_get_map_entities_with_entities_outside_zone(client):
    company = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="FarCompany",
        description="desc",
        website="https://test.com"
    )
    location = Location(
        entity_type='company',
        entity_id=company.id,
        latitude=40.0,
        longitude=0.0,
        address="Loin",
        cp="00000"
    )
    with client.application.app_context():
        db.session.add(company)
        db.session.add(location)
        db.session.commit()
    response = client.get('/map/entities?center_lat=48.85&center_lng=2.35&radius_km=1')
    assert response.status_code == 200
    assert response.json["companies"] == []

def test_get_map_entities_with_multiple_entities(client):
    company1 = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="C1",
        description="desc1",
        website="https://c1.com"
    )
    location1 = Location(
        entity_type='company',
        entity_id=company1.id,
        latitude=48.85,
        longitude=2.35,
        address="Paris",
        cp="75000"
    )
    job1 = Job(
        id=uuid.uuid4(),
        company_id=company1.id,
        title="J1",
        description="desc1",
        salary=10000,
        job_type="full_time"
    )
    location2 = Location(
        entity_type='job',
        entity_id=job1.id,
        latitude=48.85,
        longitude=2.35,
        address="Paris",
        cp="75000"
    )
    with client.application.app_context():
        db.session.add(company1)
        db.session.add(location1)
        db.session.add(job1)
        db.session.add(location2)
        db.session.commit()
    response = client.get('/map/entities?center_lat=48.85&center_lng=2.35&radius_km=1')
    assert response.status_code == 200
    assert len(response.json["companies"]) == 1
    assert len(response.json["jobs"]) == 1 