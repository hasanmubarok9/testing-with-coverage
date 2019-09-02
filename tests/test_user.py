import json
import pytest
from . import client, admin_required

class TestUser():

    def test_create_user(self, client):
        token = admin_required()
        data = {
            "username":"Kobar",
            "phonenumber":"987645343",
            "address":"Jember"
        }

        res = client.post(
            '/user/',
            data = json.dumps(data),
            headers={'Authorization': 'Bearer ' + token},
            content_type='application/json'
        )

        assert res.status_code == 200
