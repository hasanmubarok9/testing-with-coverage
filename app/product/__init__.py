from flask import Blueprint
from flask_restful import Api
from .views import Product

product = Blueprint('product', __name__)
api = Api(product)

api.add_resource(Product, '/<id>')