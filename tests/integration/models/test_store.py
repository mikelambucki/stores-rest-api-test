from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest

class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('StoreName')
            item = ItemModel('ItemName', 19.99, 1)

            self.assertIsNone(StoreModel.find_by_name('StoreName'), "Expected: None Result: Found existing store")
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('StoreName'), "Expected: {} Result: Not found".format(store.name))

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('StoreName'))

    # Can test with items, can test empty (boundary testing)
    def test_json(self):
        with self.app_context():
            store = StoreModel('StoreName')
            item = ItemModel('ItemName', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {'id': 1, 'name': 'StoreName', 'items': [{'name': 'ItemName', 'price': 19.99}]}

            self.assertDictEqual(store.json(), expected)

    def test_item_relationship(self):
        with self.app_context():
            store = StoreModel('StoreName')
            item = ItemModel('ItemName', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'ItemName')