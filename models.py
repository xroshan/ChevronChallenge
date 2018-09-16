import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Certification(db.Model):
    __tablename__ = "certification"
    id = db.Column(db.Integer, primary_key=True)

    e_type_id = db.Column(db.Integer, db.ForeignKey("equipment_type.id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"), nullable=False)

    def __init__(self, e_type_id, worker_id):
        self.e_type_id = e_type_id
        self.worker_id = worker_id

    def __repr__(self):
        return f'<Certification {self.id}, Worker: {self.worker_id}>'

    def __str__(self):
        e_type = Equipment.query.get(self.e_type_id)
        worker = Worker.query.get(self.worker_id)

        return f'<Certification {self.id}, Type: {e_type.name}, Worker: {worker.name}>'

class Equipment(db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True)

    equipment_type_id = db.Column(db.Integer, db.ForeignKey("equipment_type.id"), nullable=False)
    facility_id = db.Column(db.Integer, db.ForeignKey("facility.id"), nullable=False)
    orders = db.relationship("Order", backref="equipment", lazy=True)

    def __init__(self, e_type_id, facility_id):
        self.equipment_type_id = e_type_id
        self.facility_id = facility_id

    def __repr__(self):
        return f'<Equipment {self.id}>'

class EquipmentType(db.Model):
    __tablename__ = "equipment_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    prob = db.Column(db.Float, nullable=False)
    hour_min = db.Column(db.Integer, nullable=False)
    hour_max = db.Column(db.Integer, nullable=False)

    equipments = db.relationship("Equipment", backref="equipment_type", lazy=True)
    certifications = db.relationship("Certification", backref="equipment_type", lazy=True)

    def __init__(self, name, prob, hour_min, hour_max):
        self.name = name
        self.prob = prob
        self.hour_min = hour_min
        self.hour_max = hour_max

    def __repr__(self):
        return f'<Equipment Type {self.name}>'
    

class Facility(db.Model):
    __tablename__ = "facility"
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    equipments = db.relationship("Equipment", backref="facility", lazy=True)
    orders = db.relationship("Order", backref="facility", lazy=True)

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f'<Facility {self.id}>'

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Float, nullable=False)
    time_to_completion = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime,  default=db.func.current_timestamp(), nullable=False)
    status = db.Column(db.String(15), default="pending", nullable=False)
    est_end_time = db.Column(db.DateTime)
    est_start_time = db.Column(db.DateTime)

    facility_id = db.Column(db.Integer, db.ForeignKey("facility.id"), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"))

    def __init__(self, priority, time_to_completion, facility_id, equipment_id):
        self.priority = priority
        self.time_to_completion = time_to_completion
        self.facility_id = facility_id
        self.equipment_id = equipment_id

    def __repr__(self):
        return f'<Work Order {self.id}, {self.status}>'

class Worker(db.Model):
    __tablename__ = "worker"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shift = db.Column(db.String(15), nullable=False)
    time_until_free = db.Column(db.DateTime)

    certifications = db.relationship("Certification", backref="worker", lazy=True)
    orders = db.relationship("Order", backref="worker", lazy=True)

    def __init__(self, name, shift):
        self.name = name
        self.shift = shift

    def __repr__(self):
        return f'<Worker {self.name}>'
