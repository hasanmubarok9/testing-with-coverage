from app import db
from datetime import datetime
from flask_restful import fields

class Users(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    phonenumber = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    response_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'phonenumber': fields.String,
        'address': fields.String
    }

    def __init__(self, username, password, phonenumber, address, role="user"):
        self.username = username
        self.phonenumber = phonenumber
        self.address = address
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.id

    @classmethod
    def is_exists(cls, data):

        all_data = cls.query.all()

        existing_username = [item.username for item in all_data]

        if data in existing_username:
            return True

        return False