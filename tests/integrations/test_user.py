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

        ################
        #test login admin
        ################

        # 1 success

        data = {
            "username": "admin",
            "password": "admin"
        }


        res = client.post(
            '/user/login',
            data=json.dumps(data),
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200
        assert res_json['token'] is not None
        token_admin = res.json['token']

        # 2 failed wrong password

        data = {
            "username": "admin",
            "password": "wrongpassword"
        }

        res = client.post(
            '/user/login',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert res.status_code == 422

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

        # test create user failed (user already exist)

        data = {
            "username": "Kobar",
            "password": "kodingbareng",
            "phonenumber": "987645343",
            "address": "Jember"
        }

        res = client.post(
            '/user/',
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + token_admin},
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 422

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

        ################
        # test get user
        ################

        # 1 failed, id is empty

        res = client.get(
            '/user/',
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + token_admin},
            content_type='application/json'
        )

        assert res.status_code == 400

        # 2 success

        res = client.get(
            '/user/' + str(id_user_test),
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + token_admin},
            content_type='application/json'
        )

        assert res.status_code == 200

        #test delete user

        res = client.delete(
            '/user/' + str(id_user_test),
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + token_admin},
            content_type='application/json'
        )

        assert res.status_code == 200