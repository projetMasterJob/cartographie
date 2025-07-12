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

def test_get_companies_empty(client):
    response = client.get('/companies')
    assert response.status_code == 200
    assert response.json == []

def test_get_company_by_id_not_found(client):
    random_id = uuid.uuid4()
    response = client.get(f'/companies/{random_id}')
    assert response.status_code == 404

def test_get_company_by_id_invalid_uuid(client):
    response = client.get('/companies/invalid-uuid')
    assert response.status_code == 404

def test_get_companies_with_one(client):
    company = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="TestEntreprise",
        description="desc",
        website="https://test.com"
    )
    with client.application.app_context():
        db.session.add(company)
        db.session.commit()
    response = client.get('/companies')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "TestEntreprise"
    assert response.json[0]["location"] is None

def test_get_company_by_id_found(client):
    company = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="TestEntreprise",
        description="desc2",
        website="https://test2.com"
    )
    with client.application.app_context():
        db.session.add(company)
        db.session.commit()
        company_id = company.id
    response = client.get(f'/companies/{company_id}')
    assert response.status_code == 200
    assert response.json["name"] == "TestEntreprise"
    assert response.json["location"] is None
    assert response.json["jobs"] == []

def test_get_company_with_location(client):
    company = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="WithLocation",
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
        company_id = company.id
    response = client.get(f'/companies/{company_id}')
    assert response.status_code == 200
    assert response.json["location"]["address"] == "Paris"

def test_get_company_with_jobs(client):
    company = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="WithJobs",
        description="desc",
        website="https://test.com"
    )
    job1 = Job(
        id=uuid.uuid4(),
        company_id=company.id,
        title="Job1",
        description="desc job1",
        salary=10000,
        job_type="full_time"
    )
    job2 = Job(
        id=uuid.uuid4(),
        company_id=company.id,
        title="Job2",
        description="desc job2",
        salary=20000,
        job_type="part_time"
    )
    with client.application.app_context():
        db.session.add(company)
        db.session.add(job1)
        db.session.add(job2)
        db.session.commit()
        company_id = company.id
    response = client.get(f'/companies/{company_id}')
    assert response.status_code == 200
    assert len(response.json["jobs"]) == 2
    titles = [job["title"] for job in response.json["jobs"]]
    assert "Job1" in titles and "Job2" in titles

def test_get_companies_multiple(client):
    company1 = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="C1",
        description="desc1",
        website="https://c1.com"
    )
    company2 = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="C2",
        description="desc2",
        website="https://c2.com"
    )
    with client.application.app_context():
        db.session.add(company1)
        db.session.add(company2)
        db.session.commit()
    response = client.get('/companies')
    assert response.status_code == 200
    names = [c["name"] for c in response.json]
    assert "C1" in names and "C2" in names 