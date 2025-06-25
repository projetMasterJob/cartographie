from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sqlalchemy import text
import os

load_dotenv()

from config import Config
from extensions import db  # ✅ import propre depuis extensions.py

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)  # ✅ on initialise ici

def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        print("Connexion à la base de données OK")
    except Exception as e:
        print("Erreur de connexion à la BDD :", e)

@app.route('/')
def home():
    return jsonify({"message": "Bienvenue !"})

@app.route('/companies', methods=['GET'])
def get_companies():
    from models.company import Company  # import local pour éviter des surprises
    companies = Company.query.all()
    return jsonify([c.to_dict() for c in companies])

if __name__ == '__main__':
    with app.app_context():
        test_db_connection()
    app.run(debug=True)