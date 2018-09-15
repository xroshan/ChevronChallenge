import json

from flask import Flask, jsonify, request, send_file
from models import *

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
        data = json.loads(request.data)

        worker = Worker(data['name'], data['shift'])
        db.session.add(worker)
        
        return jsonify(worker)
    
    else:
        # get request
        workers = Worker.query.all()

        return jsonify(workers)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=True)