import json

from flask import Flask, jsonify, request, send_file
from models import *
from helpers import get_dict, get_dict_array

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/api/worker", methods=["GET", "POST"])
def worker_root():
    
    if request.method == "POST":
        # expected data [name, shift]
        data = request.get_json()

        worker = Worker(data['name'], data['shift'])
        db.session.add(worker)
        db.session.commit()
        
        return jsonify(get_dict(worker))
    
    else:
        # get request
        workers = Worker.query.all()

        return jsonify(get_dict_array(workers))

@app.route("/api/facility", methods=["GET", "POST"])
def facility_root():

    if request.method == "POST":
        # expected data [lat, lon]
        data = request.get_json()

        facility = Facility(data['lat'], data['lon'])
        db.session.add(facility)
        db.session.commit()

        return jsonify(get_dict(facility))

    else:
        # get facilities
        facilities = Facility.query.all()

        return jsonify(get_dict_array(facilities))

@app.route("/api/certification", methods=["GET", "POST"])
def certification_root():

    if request.method == "POST":
        # expected data [equipment_type_id, worker_id]
        data = request.get_json()

        certification = Certification(data['equipment_type_id'], data['worker_id'])
        db.session.add(certification)
        db.session.commit()

        return jsonify(get_dict(certification))

    else:
        # get facilities
        certifications = Certification.query.all()

        return jsonify(get_dict_array(certifications))

@app.route("/api/equipment_type", methods=["GET", "POST"])
def equipment_type_root():

    if request.method == "POST":
        # expected data [name]
        data = request.get_json()

        e_type = EquipmentType(data['name'])
        db.session.add(e_type)
        db.session.commit()

        return jsonify(get_dict(e_type))
    
    else:
        # get equipments
        equipment_types = EquipmentType.query.all()

        return jsonify(get_dict_array(equipment_types))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=True)