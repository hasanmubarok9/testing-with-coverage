import json
import pytest
from . import client, admin_required

class TestUser():

    def test_product_type(self, client):
        # add
        token = admin_required()
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

        assert res.status_code == 200