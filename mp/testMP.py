import unittest
from flask import url_for
import flask
from main import app

class MyTestForMP(unittest.TestCase):
    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass


    # code that is executed after all tests in one tes    
    # clean up logic for the test suite declared in the test modulet run
    @classmethod
    def tearDownClass(cls):
        pass

    # code that is executed before each test
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # Turn on testing
        self.app.testing = True

    # code that is executed after each test
    def tearDown(self):
        pass
    
    def test_get_page_status(self):
        pages = ['/', '/register', '/login', '/myprofile', '/logout', '/cars']
        for page in pages:
            result = self.app.get(page)
            self.assertEqual(result.status_code, 200)

    def test_post_page_status(self):
        pages = ['/book', '/processbook', '/cancelbook']
        for page in pages:
            result = self.app.get(page)
            self.assertEqual(result.status_code, 405)

    def test_home_page(self):
        response = self.app.get('/')
        self.assertIn(b'Car Share', response.data)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertIn(b'Login', response.data)
    
    def test_register_page(self):
        response = self.app.get('/register')
        self.assertIn(b'Register', response.data)

    def test_users_login(self):
        # sends POST request to login with dictionary data
        result = self.app.post('/login', data=dict(username='Nicole', password='abc123'), follow_redirects=True)

        # assert the response data
        self.assertIn(b'Nicole', result.data)

if __name__ == "__main__":
    unittest.main()