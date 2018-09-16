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

        # sanitization
        if not data:
            return jsonify({"success": False, "message": "Missing body."}), 400

        if not 'equipment_type_id' in data or not 'worker_id' in data:
            return jsonify({"success": False, "message": "Missing body fields."}), 400

        if not isinstance(data['equipment_type_id'], int) or not isinstance(data['worker_id'], int):
            return jsonify({"success": False, "message": "Invalid body fields."}), 400

        if not EquipmentType.query.get(data['equipment_type_id']):
            return jsonify({"success": False, "message": "Equipment Type key not found."}), 404

        if not Worker.query.get(data['worker_id']):
            return jsonify({"success": False, "message": "Worker key not found."}), 404

        # add to db
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

        # sanitization
        if not data:
            return jsonify({"success": False, "message": "Missing body."}), 400

        if not 'equipment_type_id' in data or not 'facility_id' in data:
            return jsonify({"success": False, "message": "Missing body fields."}), 400

        if not isinstance(data['equipment_type_id'], int) or not isinstance(data['facility_id'], int):
            return jsonify({"success": False, "message": "Invalid body fields."}), 400

        if not EquipmentType.query.get(data['equipment_type_id']):
            return jsonify({"success": False, "message": "Equipment Type key not found."}), 404

        if not Facility.query.get(data['facility_id']):
            return jsonify({"success": False, "message": "Facility key not found."}), 404

        # add to db
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

        # sanitization
        if not data:
            return jsonify({"success": False, "message": "Missing body."}), 400

        if not 'name' in data or not 'prob' in data or not 'hour_min' in data or not 'hour_max' in data:
            return jsonify({"success": False, "message": "Missing body fields."}), 400

        if not isinstance(data['name'], str) or not isinstance(data['prob'], (int, float)) or not isinstance(data['hour_min'], int) or not isinstance(data['hour_max'], int):
            return jsonify({"success": False, "message": "Invalid body fields."}), 400

        if len(data['name'].strip()) < 1 or len(data['name']) > 25:
            return jsonify({"success": False, "message": "Name length out of range."}), 400

        if data['prob'] < 0 or data['prob'] > 1:
            return jsonify({"success": False, "message": "Probability out of range."}), 400

        if data['hour_min'] < 1:
            return jsonify({"success": False, "message": "Minimum hour out of range."}), 400

        if data['hour_max'] < 1 or data['hour_max'] < data['hour_min']:
            return jsonify({"success": False, "message": "Maximum hour out of range."}), 400

        # add to db
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

        # sanitization
        if not data:
            return jsonify({"success": False, "message": "Missing body."}), 400

        if not 'lat' in data or not 'lon' in data:
            return jsonify({"success": False, "message": "Missing body fields."}), 400

        if not isinstance(data['lat'], (int, float)) or not isinstance(data['lon'], (int, float)):
            return jsonify({"success": False, "message": "Invalid body fields."}), 400

        if data['lat'] < -90.0 or data['lat'] > 90.0:
            return jsonify({"success": False, "message": "Latitude out of range."}), 400

        if data['lon'] < -180.0 or data['lon'] > 180.0:
            return jsonify({"success": False, "message": "Longitude out of range."}), 400

        # add to db
        facility = Facility(data['lat'], data['lon'])
        db.session.add(facility)
        db.session.commit()

        return jsonify(get_dict(facility))

    else:
        # get facilities
        facilities = Facility.query.all()

        return jsonify(get_dict_array(facilities))

@app.route("/api/facility/<int:fid>")
def facility(fid):

    # get response
    facility = Facility.query.get(fid)

    if facility is None:
        return jsonify({"success": False, "message": "Facility with key not found!"}), 404

    res = get_dict(facility)

    # add relations
    res['equipments'] = []
    for e in facility.equipments:
        res['equipments'].append({"id": e.id, "name": e.equipment_type.name, "equipment_type_id": e.equipment_type_id})
    res['orders'] = get_dict_array(facility.orders)

    return jsonify(res)

@app.route("/api/order", methods=["GET", "POST"])
def order_root():

    if request.method == "POST":
        # expected data [priority, time_to_completion, facility_id, equipment_id]
        data = request.get_json()

        # sanitization
        if not data:
            return jsonify({"success": False, "message": "Missing body."}), 400

        if not 'priority' in data or not 'time_to_completion' in data or not 'facility_id' in data or not 'equipment_id' in data:
            return jsonify({"success": False, "message": "Missing body fields."}), 400

        if not isinstance(data['priority'], int) or not isinstance(data['time_to_completion'], int) or not isinstance(data['facility_id'], int) or not isinstance(data['equipment_id'], int):
            return jsonify({"success": False, "message": "Invalid body fields."}), 400

        if data['priority'] < 1 or data['priority'] > 5:
            return jsonify({"success": False, "message": "Priority out of range."}), 400

        if data['time_to_completion'] < 1:
            return jsonify({"success": False, "message": "Time to completion out of range."}), 400

        if not Equipment.query.get(data['equipment_id']):
            return jsonify({"success": False, "message": "Equipment key not found."}), 404

        if not Facility.query.get(data['facility_id']):
            return jsonify({"success": False, "message": "Facility key not found."}), 404

        # add to db
        order = Order(data['priority'], data['time_to_completion'], data['facility_id'], data['equipment_id'])
        db.session.add(order)
        db.session.commit()

        # after each call
        algo.main()

        return jsonify(get_dict(order))

    else:
        # get orders
        orders = Order.query.all()

        return jsonify(get_dict_array(orders))

@app.route("/api/order/<int:order_id>")
def order(order_id):

    # get response
    order = Order.query.get(order_id)

    if order is None:
        return jsonify({"success": False, "message": "Order with key not found!"}), 404

    # build response
    res = get_dict(order)

    # add relations
    res['worker_name'] = order.worker.name if order.worker else None

    return jsonify(res)

@app.route("/api/worker", methods=["GET", "POST"])
def worker_root():
    
    if request.method == "POST":
        # expected data [name, shift]
        data = request.get_json()

        # sanitization
        if not data:
            return jsonify({"success": False, "message": "Missing body."}), 400

        if not 'name' in data or not 'shift' in data:
            return jsonify({"success": False, "message": "Missing body fields."}), 400

        if not isinstance(data['name'], str) or not isinstance(data['shift'], str):
            return jsonify({"success": False, "message": "Invalid body fields."}), 400

        if len(data['name'].strip()) < 1 or len(data['name']) > 100:
            return jsonify({"success": False, "message": "Name length out of range."}), 400

        if len(data['shift'].strip()) < 1 or len(data['shift']) > 15:
            return jsonify({"success": False, "message": "Shift length out of range."}), 400

        # add to db
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

    if worker is None:
        return jsonify({"success": False, "message": "Worker with key not found!"}), 404

    # build response
    res = get_dict(worker)

    # add relations
    res['certifications'] = []
    for cert in worker.certifications:
        res['certifications'].append({"name": cert.equipment_type.name, "id": cert.id})
    res['orders'] = get_dict_array(worker.orders)

    return jsonify(res)
    

@app.route("/debug")
def debug_algo():

    algo.main()

    return jsonify({"success": True})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, use_reloader=True)