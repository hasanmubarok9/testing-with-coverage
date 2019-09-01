from flask import Blueprint
from flask_restful import Api
from .views import User, UserList

user = Blueprint('user', __name__)
api = Api(user)

api.add_resource(User, '/', '/<int:id>')
api.add_resource(UserList, '/list')