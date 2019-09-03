import json
import pytest
from . import client, admin_required

class TestUser():

    def test_create_user(self, client):
        data = {
            "username":"Kobar",
            "password":"kobarpass",
            "phonenumber":"987645343",
            "address":"Jember"
        }

        res = client.post(
            '/user/register',
            data = json.dumps(data),
            content_type='application/json'
        )

        assert res.status_code == 200
