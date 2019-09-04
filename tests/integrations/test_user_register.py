import json
from tests import client, reset_database

def TestUserRegister():

    reset_database()

    def test_user_register(self, client):
        data = {
            "username": "User Tria",
            "password": "user-tria-password",
            "address": "Malang",
            "phonenumber": "0123456789"
        }

        res = client.post(
            'user/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['username'] == "User Tria"