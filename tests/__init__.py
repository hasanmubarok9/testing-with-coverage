import pytest

from flask import Flask, request, json
from app import app, db, cache
from app.users.model import Users as UserModel
from app.users.views import bcrypt

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)


def reset_database():

    db.drop_all()
    db.create_all()

    admin = UserModel("admin-tria", bcrypt.generate_password_hash("triapass"), "0986463", "Balikpapan", "admin")

    # create test non-admin user

    # save users to database
    db.session.add(admin)
    db.session.commit()


def get_token_admin():
    token = cache.get('token-admin')
    if token is None:
        data = {
            'username': 'admin-tria',
            'password': 'triapass'
        }

        req = call_client(request)
        res = req.post(
            '/user/login',
            data=json.dumps(data),
            content_type='application/json'
            )

        res_json = json.loads(res.data)

        # logging.warning('RESULT : %s', res_json)

        assert res.status_code == 200

        cache.set('token-admin', res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token