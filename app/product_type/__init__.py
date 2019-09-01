from flask import Blueprint
from flask_restful import Api
from .views import ProductType

product_type = Blueprint('product_type', __name__)
api = Api(product_type)

api.add_resource(ProductType, '/<id>')