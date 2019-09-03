from tests import get_token_admin, reset_database, client
import json

class TestProduct():

    reset_database()

    token = get_token_admin()

    def test_product(self, client):

        # add product type first
        data = {
            "name": "vehicle"
        }

        # test login admin

        res = client.post(
            '/product_type/',
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + self.token},
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200
        id_product_type = res_json['id']

        data = {
            "name": "car",
            "product_type_id": id_product_type,
            "created_by": 1
        }

        # test login admin

        res = client.post(
            '/product/',
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + self.token},
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200
        id_product = res_json['id']

        # test get product

        res = client.get(
            '/product/' + str(id_product),
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + self.token},
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

        data = {
            "name": "bus",
            "product_type_id": id_product_type
        }

        # test login admin

        res = client.put(
            '/product/' + str(id_product),
            data=json.dumps(data),
            headers={'Authorization': 'Bearer ' + self.token},
            content_type='application/json'
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200