from flask_restful import Resource, marshal, reqparse
from app import db, app
from .model import ProductType as ProductTypeModel
from app.baseview import BaseCrud, BaseViewList
from flask_jwt_extended import jwt_required, get_jwt_claims
from app.util import admin_required

class GetEditDelete(BaseCrud, Resource):

    def __init__(self):
        super(GetEditDelete).__init__(ProductTypeModel)

    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        data = parser.parse_args()

        user = ProductTypeModel(data['name'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, ProductTypeModel.response_fields), 200, {'Content-Type': 'application/json'}

    @admin_required
    def put(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        args = parser.parse_args()
        qry = ProductTypeModel.query.get(id)
        if qry is None:
            return {'status': 'Product Type Not Found'}, 404, {'Content-Type': 'application/json'}

        setattr(qry, 'name', args['name'])

        db.session.commit()

class ViewList(BaseViewList, Resource):

    def __init__(self):
        super(ViewList, self).__init__(ProductTypeModel)
