from flask_restful import Resource, Api, reqparse, marshal, inputs
from app import db, app
from .model import Users as UserModel
from app.baseview import BaseCrud, BaseViewList

class GetEditDelete(BaseCrud, Resource):

    def __init__(self):
        super(GetEditDelete, self).__init__(UserModel)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('phonenumber', location='json')
        parser.add_argument('address', location='json', required=True)
        data = parser.parse_args()

        user = UserModel(data['name'], data['age'], data['sex'], data['client_id'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, UserModel.response_fields), 200, {'Content-Type': 'application/json'}

    def put(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('phonenumber', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        args = parser.parse_args()

        qry = UserModel.query.get(id)
        if qry is None:
            return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}

        setattr(qry, 'username', args['username'])
        setattr(qry, 'phonenumber', args['phonenumber'])
        setattr(qry, 'address', args['address'])

        db.session.commit()

        return marshal(qry, UserModel.response_fields), 200, {'Content-Type': 'application/json'}

class ViewList(BaseViewList, Resource):

    def __init__(self):
        super(ViewList, self).__init__(UserModel)
