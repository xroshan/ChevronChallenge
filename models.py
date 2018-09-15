import os
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Worker(db.Model):
    __tablename__ = "worker"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shift = db.Column(db.String(15), nullable=False)

    certifications = db.relationship("Certification", backref="worker", lazy=True)
    orders = db.relationship("Order", backref="worker", lazy=True)

class Facility(db.Model):
    __tablename__ = "facility"
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    equipments = db.relationship("Equipment", backref="facility", lazy=True)
    orders = db.relationship("Order", backref="facility", lazy=True)

class Equipment(db.Model):
    __tablename__ = "equipment"
    id = db.Column(db.Integer, primary_key=True)
    equipment_type = db.Column(db.String(25), nullable=False)
    prob = db.Column(db.Float, nullable=False)
    hour_min = db.Column(db.Integer, nullable=False)
    hour_max = db.Column(db.Integer, nullable=False)

    facility = db.Column(db.Integer, db.ForeignKey("facility.id"), nullable=False)
    orders = db.relationship("Order", backref="equipment", lazy=True)

class Certification(db.Model):
    __tablename__ = "certification"
    id = db.Column(db.Integer, primary_key=True)
    equipment_type = db.Column(db.String(25), nullable=False)

    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"), nullable=False)
    
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Float, nullable=False)
    time_to_completion = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    status = db.Column(db.String(15), nullable=False)

    facility_id = db.Column(db.Integer, db.ForeignKey("facility.id"), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("worker.id"), nullable=False)
