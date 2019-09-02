import json
import pytest
from tests import client, reset_database

class TestUser():

    reset_database()

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
