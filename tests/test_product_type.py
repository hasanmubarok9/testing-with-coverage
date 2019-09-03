import json
import pytest
from . import client, admin_required, reset_database

class TestUser():

    reset_database()

    def test_product_type(self, client):

        # test register admin
        data = {
            "username": "admin-trya",
            "password": "tryapass",
            "phonenumber": "0123456789",
            "address": "Malang",
            "role": "admin"
        }

        res = client.post(
            '/user/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['data']['username'] == 'admin-trya'

        data = {
            "username": "admin-trya",
            "password": "tryapass"
        }

        # test login admin

        res = client.post(
            '/user/login',
            data=json.dumps(data),
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200
        assert res_json['token'] is not None
        token = res.json['token']

        # add
        data = {
            "name":"makanan"
        }

        res = client.post(
            '/product_type/',
            data = json.dumps(data),
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
        )

        res_json = json.loads(res.data)
        id = res_json['id']
        assert res.status_code == 200
        assert res_json['name'] == 'makanan'


        # edit
        data = {
            "name":"food"
        }

        res = client.put(
            '/product_type/' + str(id),
            data = json.dumps(data),
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
        )

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['name'] == 'food'


        # view list
        data = {}
        res = client.post(
            '/product_type/list',
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
        )

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json[0]['name'] == 'food'