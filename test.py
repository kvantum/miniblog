import os
import tempfile
import unittest

import miniblog
import miniblog.db

class MiniblogTestCase(unittest.TestCase):

    def setUp(self):
		"""
		Prepare the initial data for tests
		"""
		self.db_fd, miniblog.app.config['DATABASE'] = tempfile.mkstemp()
		self.app = miniblog.app.test_client()
		miniblog.db.init_db()

    def tearDown(self):
		"""
		Delete the preparation data for tests
		"""
		os.close(self.db_fd)
		os.unlink(miniblog.app.config['DATABASE'])
	
    def test_connect(self):
		"""
		Connect to database
		"""
		self.assertIsNotNone(self.db_fd)
				        
    def test_empty_db(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('No entries here so far', response.data)

    def test_render_login(self):
        """
        Test if login page is rendered
        """
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login', response.data)
        self.assertIn('Password', response.data)
    
    def login(self, username, password):
		return self.app.post('/login', data=dict(
		username=username,
		password=password
		), follow_redirects=True)
        
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    def test_login_logout(self):
		"""
		Login and logout checking
		"""
		response = self.login('admin', 'admin')
		self.assertIn('You were logged in', response.data)
		response = self.logout()
		self.assertIn('You were logged out', response.data)
		response = self.login('adminx', 'admin')
		self.assertIn('Invalid password or username', response.data)
		response = self.login('admin', 'adminx')
		self.assertIn('Invalid password or username', response.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
