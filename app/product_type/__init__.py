from flask import Blueprint
from flask_restful import Api
from .views import GetEditDelete, ViewList

product_type = Blueprint('product_type', __name__)
api = Api(product_type)

api.add_resource(GetEditDelete, '/','/<id>')
api.add_resource(ViewList, '/list')
