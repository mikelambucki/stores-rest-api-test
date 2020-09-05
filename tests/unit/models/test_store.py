from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_init(self):
        store = StoreModel('Name')

        self.assertEqual(store.name, 'Name', 'Expected: Name Actual: {}'.format(store.name))
