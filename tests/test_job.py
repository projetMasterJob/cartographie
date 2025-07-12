import pytest
from app import create_app, db
from models.job import Job
from models.company import Company
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

def test_get_jobs_empty(client):
    response = client.get('/jobs')
    assert response.status_code == 200
    assert response.json == []

def test_get_job_by_id_not_found(client):
    random_id = uuid.uuid4()
    response = client.get(f'/jobs/{random_id}')
    assert response.status_code == 404

def test_get_job_by_id_invalid_uuid(client):
    response = client.get('/jobs/invalid-uuid')
    assert response.status_code == 404

def test_get_jobs_with_one(client):
    job = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="TestJob",
        description="desc job",
        salary=30000,
        job_type="full_time"
    )
    with client.application.app_context():
        db.session.add(job)
        db.session.commit()
    response = client.get('/jobs')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "TestJob"
    assert response.json[0]["location"] is None

def test_get_job_by_id_found(client):
    job = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="TestJob2",
        description="desc job2",
        salary=35000,
        job_type="part_time"
    )
    with client.application.app_context():
        db.session.add(job)
        db.session.commit()
        job_id = job.id
    response = client.get(f'/jobs/{job_id}')
    assert response.status_code == 200
    assert response.json["title"] == "TestJob2"
    assert response.json["location"] is None
    assert response.json["company_name"] is None or isinstance(response.json["company_name"], str)

def test_get_job_with_location(client):
    job = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="WithLocation",
        description="desc",
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
        job_id = job.id
    response = client.get(f'/jobs/{job_id}')
    assert response.status_code == 200
    assert response.json["location"]["address"] == "Paris"

def test_get_job_with_company(client):
    company = Company(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        name="CompanyForJob",
        description="desc",
        website="https://test.com"
    )
    job = Job(
        id=uuid.uuid4(),
        company_id=company.id,
        title="JobWithCompany",
        description="desc job",
        salary=20000,
        job_type="full_time"
    )
    with client.application.app_context():
        db.session.add(company)
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        company_image_url = company.image_url
    response = client.get(f'/jobs/{job_id}')
    assert response.status_code == 200
    assert response.json["company_name"] == "CompanyForJob"
    assert response.json["company_image_url"] == company_image_url

def test_get_jobs_multiple(client):
    job1 = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="J1",
        description="desc1",
        salary=10000,
        job_type="full_time"
    )
    job2 = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="J2",
        description="desc2",
        salary=20000,
        job_type="part_time"
    )
    with client.application.app_context():
        db.session.add(job1)
        db.session.add(job2)
        db.session.commit()
    response = client.get('/jobs')
    assert response.status_code == 200
    titles = [j["title"] for j in response.json]
    assert "J1" in titles and "J2" in titles 