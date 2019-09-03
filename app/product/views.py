from flask_restful import Resource, Api, reqparse, marshal, inputs
from app import db, app
from flask_jwt_extended import jwt_required, get_jwt_claims
from .model import Product as ProductModel
from app.baseview import BaseCrud, BaseViewList

class GetEditDelete(BaseCrud, Resource):

    def __init__(self):
        super(GetEditDelete, self).__init__(ProductModel)

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('product_type_id', location='json', required=True)
        parser.add_argument('created_by', location='json', required=True)
        data = parser.parse_args()

        claims = get_jwt_claims()

        product = ProductModel(data['name'], data['product_type_id'], data['created_by'])
        db.session.add(product)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product)

        return marshal(product, ProductModel.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
    def put(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('product_type_id', location='json', required=True)
        args = parser.parse_args()
        qry = ProductModel.query.get(id)
        if qry is None:
            return {'status': 'Product Not Found'}, 404, {'Content-Type': 'application/json'}

        setattr(qry, 'name', args['name'])
        setattr(qry, 'product_type_id', args['product_type_id'])

        db.session.commit()

class ViewList(BaseViewList, Resource):

    def __init__(self):
        super(ViewList, self).__init__(ProductModel)