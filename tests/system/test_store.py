from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json;

class StoreTest(BaseTest):

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/{}'.format('test'), data={'name': 'test'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/{}'.format('test'), data={'name': 'test'})
                response = client.post('/store/{}'.format('test'), data={'name': 'test'})

                self.assertEqual(response.status_code, 400)
                self.assertEqual(json.loads(response.data),
                                 {'message': "A store with name 'test' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/{}'.format('test'), data={'name': 'test'})
                response = client.delete('/store/{}'.format('test'), data={'name': 'test'})

                self.assertEqual(json.loads(response.data), {'message': 'Store deleted'})


    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/{}'.format('test'), data={'name': 'test'})
                response = client.get('/store/{}'.format('test'), data={'name': 'test'})

                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/{}'.format('test'), data={'name': 'test'})

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test')
                item = ItemModel('ItemName', 19.99, 1)

                store.save_to_db()
                item.save_to_db()

                response = client.get('/store/{}'.format('test'), data={'name': 'test'})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'name': 'test', 'items': [{'name': 'ItemName', 'price': 19.99}]})

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/stores')

                expected = {'stores': []}

                self.assertDictEqual(json.loads(response.data), expected)


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('StoreName')
                item = ItemModel('ItemName', 19.99, 1)

                store.save_to_db()
                item.save_to_db()

                response = client.get('/stores')

                expected = {'stores': [{
                    'name': 'StoreName',
                    'items': [{'name': 'ItemName', 'price': 19.99}]
                }]}

                self.assertDictEqual(json.loads(response.data), expected)