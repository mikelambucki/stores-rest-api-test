from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):

    def test_user_init(self):
        user = UserModel('User', 'Password')

        self.assertEqual(user.username, 'User', 'Expected: {} Result: {}'.format('User', user.username))
        self.assertEqual(user.password, 'Password', 'Expected: {} Result: {}'.format('Password', user.password))