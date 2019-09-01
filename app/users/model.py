from app import db
from flask_restful import fields

class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    response_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'phonenumber': fields.String,
        'address': fields.String
    }

    def __init__(self, username, phonenumber, address):
        self.username = username
        self.phonenumber = phonenumber
        self.address = address

    def __repr__(self):
        return '<User %r>' % self.id