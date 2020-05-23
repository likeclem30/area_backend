from sqlalchemy import func
from areas_backend.db import db


class AreaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    areacode = db.Column(db.String(250))
    area = db.Column(db.String(250))
    zonecode = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, server_default=func.now())
