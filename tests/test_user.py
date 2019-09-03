import json
import pytest
from tests import client, reset_database

class TestUser():

    reset_database()

    def test_admin(self, client):

        #test register admin

        data = {
            "username": "admin",
            "password": "admin",
            "phonenumber": "0987635343",
            "address": "Bimasakti",
            "role": "admin"
        }

        res = client.post(
            '/user/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['data']['username'] == 'admin'

        data = {
            "username": "admin",
            "password": "admin"
        }

        #test login admin

        res = client.post(
            '/user/login',
            data=json.dumps(data),
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200
        assert res_json['token'] is not None
        token_admin = res.json['token']

        # test create user by admin

        data = {
            "username":"Kobar",
            "password": "kodingbareng",
            "phonenumber":"987645343",
            "address":"Jember"
        }

        res = client.post(
            '/user/',
            data = json.dumps(data),
            headers={'Authorization': 'Bearer ' + token_admin},
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200
        id_user_test = res_json['data']['id']

        # test update user by admin

        data = {
            "username": "kobur",
            "password": "kodingkabur",
            "phonenumber": "987645343",
            "address": "Malang"
        }

        res = client.put(
            '/user/' + str(id_user_test),
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + token_admin},
            content_type='application/json'
        )

        assert res.status_code == 200