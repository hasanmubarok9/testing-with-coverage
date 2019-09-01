from flask import Blueprint
from flask_restful import Api
from .views import GetEditDelete, ViewList

user = Blueprint('user', __name__)
api = Api(user)

api.add_resource(GetEditDelete, '/', '/<int:id>')
api.add_resource(ViewList, '/list')