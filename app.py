from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sqlalchemy import text
import os
from math import cos, radians

load_dotenv()

from config import Config
from extensions import db
from models.company import Company
from models.job import Job
from models.location import Location

def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        print("Connexion à la base de données OK")
    except Exception as e:
        print("Erreur de connexion à la BDD :", e)

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Bienvenue !"})

    @app.route('/companies', methods=['GET'])
    def get_companies():
        companies = Company.query.all()
        result = []
        for company in companies:
            company_dict = company.to_dict()
            location = Location.query.filter_by(
                entity_type='company', 
                entity_id=company.id
            ).first()
            company_dict['location'] = location.to_dict() if location else None
            result.append(company_dict)
        return jsonify(result)

    @app.route('/companies/<uuid:company_id>', methods=['GET'])
    def get_company(company_id):
        company = Company.query.get_or_404(company_id)
        company_dict = company.to_dict()
        location = Location.query.filter_by(
            entity_type='company', 
            entity_id=company.id
        ).first()
        company_dict['location'] = location.to_dict() if location else None
        jobs = Job.query.filter_by(company_id=company.id).all()
        company_dict['jobs'] = [job.to_dict() for job in jobs]
        return jsonify(company_dict)

    @app.route('/jobs', methods=['GET'])
    def get_jobs():
        jobs = Job.query.all()
        result = []
        for job in jobs:
            job_dict = job.to_dict()
            location = Location.query.filter_by(
                entity_type='job', 
                entity_id=job.id
            ).first()
            job_dict['location'] = location.to_dict() if location else None
            result.append(job_dict)
        return jsonify(result)

    @app.route('/jobs/<uuid:job_id>', methods=['GET'])
    def get_job(job_id):
        job = Job.query.get_or_404(job_id)
        job_dict = job.to_dict()
        location = Location.query.filter_by(
            entity_type='job', 
            entity_id=job.id
        ).first()
        job_dict['location'] = location.to_dict() if location else None
        company = db.session.get(Company, job.company_id)
        if company:
            job_dict['company_name'] = company.name
            job_dict['company_image_url'] = company.image_url
        else:
            job_dict['company_name'] = None
            job_dict['company_image_url'] = None
        return jsonify(job_dict)

    @app.route('/map/entities', methods=['GET'])
    def get_entities_in_map_zone():
        center_lat = request.args.get('center_lat', type=float)
        center_lng = request.args.get('center_lng', type=float)
        zoom_level = request.args.get('zoom_level', type=int, default=12)
        radius_km = request.args.get('radius_km', type=float)
        if center_lat is None or center_lng is None:
            return jsonify({'error': 'center_lat et center_lng sont requis'}), 400
        if not radius_km:
            radius_km = 50.0 / (2 ** (zoom_level - 10))
        lat_delta = radius_km / 111.0
        lng_delta = radius_km / (111.0 * cos(radians(center_lat)))
        locations = Location.query.filter(
            Location.latitude.between(center_lat - lat_delta, center_lat + lat_delta),
            Location.longitude.between(center_lng - lng_delta, center_lng + lng_delta)
        ).all()
        companies = []
        jobs = []
        for location in locations:
            if location.entity_type == 'company':
                company = db.session.get(Company, location.entity_id)
                if company:
                    company_dict = company.to_dict()
                    company_dict['location'] = location.to_dict()
                    companies.append(company_dict)
            elif location.entity_type == 'job':
                job = db.session.get(Job, location.entity_id)
                if job:
                    job_dict = job.to_dict()
                    job_dict['location'] = location.to_dict()
                    jobs.append(job_dict)
        return jsonify({
            'center': {
                'lat': center_lat,
                'lng': center_lng
            },
            'radius_km': radius_km,
            'zoom_level': zoom_level,
            'companies': companies,
            'jobs': jobs,
            'total_entities': len(companies) + len(jobs)
        })

    return app

# Initialisation de l'app uniquement pour le déploiement (Vercel, production, etc.)
# et pas lors de l'import pour les tests
import os
if __name__ == "__main__":
    app = create_app()
    app.run()
# Pour Vercel ou d'autres serveurs WSGI, expose l'app uniquement si ce n'est pas en import de test
if "VERCEL" in os.environ or os.getenv("DYNO") or os.getenv("GUNICORN_CMD_ARGS"):
    app = create_app()