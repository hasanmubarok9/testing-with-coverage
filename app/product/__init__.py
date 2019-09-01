from flask import Blueprint
from flask_restful import Api
from .views import GetEditDelete, ViewList

product = Blueprint('product', __name__)
api = Api(product)

api.add_resource(GetEditDelete, '/','/<id>')
api.add_resource(ViewList, '/list')