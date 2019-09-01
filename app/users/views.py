from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import  desc
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
        parser.add_argument('phonenumber', location='json', required=True)
        parser.add_argument('address', location='json', required=True)
        data = parser.parse_args()

        user = UserModel(data['username'], data['phonenumber'], data['address'])
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

    def delete(self, id):
        qry = UserModel.query.get(id)
        if qry is None:
            return {'status': 'User Not Found'}, 404, {'Content-Type': 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'User Deleted'}, 200, {'Content-Type': 'application/json'}


class UserList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('orderby', location='args', choices=('id', 'username'))
        parser.add_argument('sort', location='args', choices=('asc', 'desc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = UserModel.query

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(UserModel.id))  # bisa gini
                else:
                    qry = qry.order_by((UserModel.id))
            elif args['orderby'] == 'username':
                if args['sort'] == 'desc':
                    qry = qry.order_by((UserModel.id).desc())  # bisa juga gini
                else:
                    qry = qry.order_by((UserModel.id))

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, UserModel.response_fields))
        return rows, 200, {'Content-Type': 'application/json'}