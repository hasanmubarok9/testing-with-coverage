from app import db
from datetime import datetime
from flask_restful import fields

class ProductType(db.Model):
    __tablename__ = "product_type"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    response_fields = {
        'id': fields.Integer,
        'name': fields.String
    }

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ProductType %r>' % self.id