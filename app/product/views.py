from flask_restful import Resource, marshal
from .model import Product as ProductModel

class Product(Resource):

    def __init__(self):
        pass

    def get(self, id):
        qry = ProductModel.query.get(id)
        if qry is not None:
            return marshal(qry, ProductModel.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}