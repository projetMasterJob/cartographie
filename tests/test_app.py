import pytest
from app import create_app, db

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

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Bienvenue !"}

def test_db_connection_coverage():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        from app import test_db_connection
        test_db_connection()