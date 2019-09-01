from flask_restful import Resource, Api, reqparse, marshal, inputs
from app import db, app
from .model import Users as UserModel

class User(Resource):

    def __init__(self):
        pass

    def get(self, id=None):
        if id is not None:
            qry = UserModel.query.get(id)
            if qry is not None:
                return marshal(qry, UserModel.response_fields), 200, {'Content-Type': 'application/json'}
            return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}
        else:
            return {'status': 'id Please'}, 400, {'Content-Type': 'application/json'}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('phonenumber', location='json')
        parser.add_argument('address', location='json', required=True)
        data = parser.parse_args()

        user = UserModel(data['username'], data['phonenumber'], data['address'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, UserModel.response_fields), 200, {'Content-Type': 'application/json'}


class UserList(Resource):
    pass