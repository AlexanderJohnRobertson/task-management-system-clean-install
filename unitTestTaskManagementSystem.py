import unittest
from app import app

'''Unit test for the Task Management System'''

class TestRoutes(unittest.TestCase):
    def setUp(self): # Set up the app for testing
        self.app = app.test_client()

    def test_login(self): # Test the login route
        response = self.app.get('login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log', response.data)

    def test_create_account(self): # Test the create account route
        response = self.app.get('createaccount')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create', response.data)

    def test_add_task(self): # Test the add task route
        response = self.app.get('addtask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_view_task(self): # Test the view task route
        response = self.app.get('viewtasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_update_task(self): # Test the update task route
        response = self.app.get('updatetask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_delete_task(self): # Test the delete task route
        response = self.app.get('deletetask')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_create_project(self): # Test the create project route
        response = self.app.get('addproject')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_view_projects(self): # Test the view projects route
        response = self.app.get('viewprojects')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_update_project(self): # Test the update project route
        response = self.app.get('updateproject')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_delete_project(self): # Test the delete project route
        response = self.app.get('deleteproject')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_account_details(self): # Test the account details route
        response = self.app.get('accountdetails')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_update_account_details(self): # Test the update account details route
        response = self.app.get('updateaccountdetails')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_change_username(self): # Test the change username route
        response = self.app.get('changeusername')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_change_password(self): # Test the change password route
        response = self.app.get('changepassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_view_account_details(self): # Test the view account details route
        response = self.app.get('accountdetails')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_user_home(self): # Test the user home route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'', response.data)

    def test_view_users(self): # Test the view users route
        response = self.app.get('viewusers')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_delete_user(self): # Test the delete user route
        response = self.app.get('deleteuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_block_user(self): # Test the block user route
        response = self.app.get('blockuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_unblock_user(self): # Test the unblock user route
        response = self.app.get('unblockuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_change_user_password(self): # Test the change user password route
        response = self.app.get('changeuserpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    def test_reset_password(self): # Test the reset password route
        response = self.app.get('reset')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access Denied', response.data)

    """def test_setup(self): # Test the setup route
        response = self.app.get('setup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'First', response.data)"""

if __name__ == '__main__':
    unittest.main() # Run the tests