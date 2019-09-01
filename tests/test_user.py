import json
import pytest
from . import client

class TestUser():

    def test_create_user(self, client):
        data = {
            "username":"Kobar",
            "phonenumber":"987645343",
            "address":"Jember"
        }

        res = client.post(
            '/user/',
            data = json.dumps(data),
            content_type='application/json'
        )

        assert res.status_code == 200
