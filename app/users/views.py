from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from app import db, app
from datetime import timedelta
from .model import Users as UserModel
from app.baseview import BaseCrud, BaseViewList
from app.util import admin_required

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):

    user = UserModel.query.get(identity)

    return {
        "role": user.role,
        "id": user.id
    }

class Register(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json', required=True, help='username must be string, unique, exist')
        parser.add_argument('password', type=str, location='json', required=True, help='password must be string and exist')
        parser.add_argument('role', type=str, location='json', required=False, help='password must be string and exist')
        parser.add_argument('address', type=str, location='json', required=True, help='address must be string and exist')
        parser.add_argument('phonenumber', type=str, location='json', required=True, help='phonenumber must be string and exist')

        args = parser.parse_args()

        pw_hash = bcrypt.generate_password_hash(args['password'])

        if args['role'] == "admin":
            role = "admin"
        else:
            role = "user"

        #validate unique username
        all_data = UserModel.query.all()

        existing_username = [item.username for item in all_data]

        if args['username'] in existing_username:
            return {'Status': 'User already exist'}, 422

        user = UserModel(
            username = args['username'],
            password = pw_hash,
            phonenumber= args['phonenumber'],
            address=args['address'],
            role=role
        )

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)


        return {"data": marshal(user, UserModel.response_fields), "message" : "Please Login to Continue"}, 200

class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)

        args = parser.parse_args()

        user = UserModel.query.filter_by(username=args['username']).first()

        if user == None:
            # if not return 401
            return {"message": "USER NOT FOUND"}, 404

        if not bcrypt.check_password_hash(user.password, args['password']):
            return {"message": "WRONG PASSWORD!!"}, 422


        # if have account create token for him
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

        # then return to him
        return {"token": token, "message": "Login success"}, 200

class GetEditDelete(BaseCrud, Resource):

    def __init__(self):
        super(GetEditDelete, self).__init__(UserModel)

    @admin_required
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

    @admin_required
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
