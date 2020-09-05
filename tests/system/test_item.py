from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                self.auth_header = "JWT {}".format(json.loads(auth_request.data)['access_token'])

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 401)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('name').save_to_db()
                ItemModel('name', 19.99, 1).save_to_db()
                resp = client.get('/item/name', headers={'Authorization': self.auth_header})
                self.assertEqual(resp.status_code, 200)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers={'Authorization': self.auth_header})
                self.assertEqual(response.status_code, 404)

    def test_post_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/item/ItemName', data={'name': 'ItemName', 'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)

    def test_post_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('StoreName').save_to_db()
                ItemModel('ItemName', 19.99, 1).save_to_db()

                response = client.post('/item/ItemName', data={'name': 'ItemName', 'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('StoreName').save_to_db()
                ItemModel('ItemName', 19.99, 1).save_to_db()
                response = client.delete('/item/ItemName', data={'name': 'ItemName', 'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)

    def test_delete_no_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.delete('/item/ItemName', data={'name': 'ItemName', 'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 404)

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                response = client.put('/item/ItemName', data={'name': 'ItemName', 'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('StoreName').save_to_db()
                ItemModel('ItemName', 19.99, 1).save_to_db()

                response = client.put('/item/ItemName', data={'name': 'ItemName', 'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)

    def test_item_list_empty(self):
        with self.app() as client:
            with self.app_context():
                expected = {'items' : []}

                response = client.get('/items')

                self.assertDictEqual(expected, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('StoreName').save_to_db()
                ItemModel('ItemName', 19.99, 1).save_to_db()

                expected = {'items': [{'name': 'ItemName', 'price': 19.99}]}

                response = client.get('/items')

                self.assertDictEqual(expected, json.loads(response.data))