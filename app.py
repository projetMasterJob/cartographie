from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sqlalchemy import text
import os

load_dotenv()

from config import Config
from extensions import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        print("Connexion à la base de données OK")
    except Exception as e:
        print("Erreur de connexion à la BDD :", e)

from models.company import Company
from models.job import Job
from models.location import Location

@app.route('/')
def home():
    return jsonify({"message": "Bienvenue !"})

@app.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([c.to_dict() for c in companies])

@app.route('/companies/<uuid:company_id>', methods=['GET'])
def get_company(company_id):
    company = Company.query.get_or_404(company_id)
    return jsonify(company.to_dict())

@app.route('/companies', methods=['POST'])
def create_company():
    data = request.json
    company = Company(
        user_id=data['user_id'],
        name=data['name'],
        description=data.get('description'),
        website=data.get('website')
    )
    db.session.add(company)
    db.session.commit()
    return jsonify(company.to_dict()), 201

@app.route('/companies/<uuid:company_id>', methods=['PUT'])
def update_company(company_id):
    company = Company.query.get_or_404(company_id)
    data = request.json
    company.name = data.get('name', company.name)
    company.description = data.get('description', company.description)
    company.website = data.get('website', company.website)
    db.session.commit()
    return jsonify(company.to_dict())

@app.route('/companies/<uuid:company_id>', methods=['DELETE'])
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    return '', 204

@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([j.to_dict() for j in jobs])

@app.route('/jobs/<uuid:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict())

@app.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    job = Job(
        company_id=data['company_id'],
        title=data['title'],
        description=data['description'],
        salary=data.get('salary'),
        job_type=data['job_type']
    )
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201

@app.route('/jobs/<uuid:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.json
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.salary = data.get('salary', job.salary)
    job.job_type = data.get('job_type', job.job_type)
    db.session.commit()
    return jsonify(job.to_dict())

@app.route('/jobs/<uuid:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return '', 204

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([l.to_dict() for l in locations])

@app.route('/locations/<uuid:location_id>', methods=['GET'])
def get_location(location_id):
    location = Location.query.get_or_404(location_id)
    return jsonify(location.to_dict())

@app.route('/locations', methods=['POST'])
def create_location():
    data = request.json
    location = Location(
        entity_type=data['entity_type'],
        entity_id=data['entity_id'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        address=data.get('address')
    )
    db.session.add(location)
    db.session.commit()
    return jsonify(location.to_dict()), 201

@app.route('/locations/<uuid:location_id>', methods=['PUT'])
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    data = request.json
    location.latitude = data.get('latitude', location.latitude)
    location.longitude = data.get('longitude', location.longitude)
    location.address = data.get('address', location.address)
    db.session.commit()
    return jsonify(location.to_dict())

@app.route('/locations/<uuid:location_id>', methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        test_db_connection()
    app.run(debug=True)