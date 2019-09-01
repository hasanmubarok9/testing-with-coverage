from app import db
from flask_restful import fields

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'product_type_id': fields.Integer
    }

    def __init__(self, name, product_type_id):
        self.name = name
        self.product_type_id = product_type_id

    def __repr__(self):
        return '<Product %r>' % self.id