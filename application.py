# main backend entry point for chevron challenge

from flask import Flask, jsonify, request, send_file
from models import *
from helpers import get_dict, get_dict_array
import algo

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return send_file("templates/index.html")

# API Endpoints, JSON request/response, TODO: validate post data

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

@app.route("/api/equipment", methods=["GET", "POST"])
def equipment_root():

    if request.method == "POST":
        # expected data [equipment_type_id, facility_id]
        data = request.get_json()

        equipment = Equipment(data['equipment_type_id'], data['facility_id'])
        db.session.add(equipment)
        db.session.commit()

        return jsonify(get_dict(equipment))

    else:
        # get equipments
        equipments = Equipment.query.all()

        return jsonify(get_dict_array(equipments))

@app.route("/api/equipment_type", methods=["GET", "POST"])
def equipment_type_root():

    if request.method == "POST":
        # expected data [name, prob, hour_min, hour_max]
        data = request.get_json()

        e_type = EquipmentType(data['name'], data['prob'], data['hour_min'], data['hour_max'])
        db.session.add(e_type)
        db.session.commit()

        # main algorithm run
        algo.main()

        return jsonify(get_dict(e_type))
    
    else:
        # get equipments
        equipment_types = EquipmentType.query.all()

        return jsonify(get_dict_array(equipment_types))

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

@app.route("/api/order", methods=["GET", "POST"])
def order_root():

    if request.method == "POST":
        # expected data [priority, time_to_completion, facility_id, equipment_id]
        data = request.get_json()

        order = Order(data['priority'], data['time_to_completion'], data['facility_id'], data['equipment_id'])
        db.session.add(order)
        db.session.commit()



        return jsonify(get_dict(order))

    else:
        # get orders
        orders = Order.query.all()

        return jsonify(get_dict_array(orders))

@app.route("/api/worker", methods=["GET", "POST"])
def worker_root():
    
    if request.method == "POST":
        # expected data [name, shift, certificaions[](optional)]
        data = request.get_json()

        worker = Worker(data['name'], data['shift'])
        db.session.add(worker)
        db.session.commit()
        
        return jsonify(get_dict(worker))
    
    else:
        # get request
        workers = Worker.query.all()

        return jsonify(get_dict_array(workers))

@app.route("/api/worker/<int:worker_id>")
def worker(worker_id):

    # get response
    worker = Worker.query.get(worker_id)

    # build response
    res = get_dict(worker)

    # add relations
    res['certifications'] = get_dict_array(worker.certifications)
    res['orders'] = get_dict_array(worker.orders)

    return jsonify(res)
    

@app.route("/debug")
def debug_algo():

    algo.main()

    return jsonify({"success": True})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=True)