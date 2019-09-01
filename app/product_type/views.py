from flask_restful import Resource, marshal
from .model import ProductType as ProductTypeModel

class ProductType(Resource):

    def __init__(self):
        pass

    def get(self, id):
        qry = ProductTypeModel.query.get(id)
        if qry is not None:
            return marshal(qry, ProductTypeModel.response_fields), 200, {'Content-Type': 'application/json'}
        return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}