from app import db
from datetime import datetime
from flask_restful import fields

class Product(db.Model):
    __tablename__ = "product"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'product_type_id': fields.Integer,
        'created_by': fields.Integer
    }

    def __init__(self, name, product_type_id, created_by):
        self.name = name
        self.product_type_id = product_type_id
        self.created_by = created_by

    def __repr__(self):
        return '<Product %r>' % self.id