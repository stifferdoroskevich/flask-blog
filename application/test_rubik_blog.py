import os
import flask_blog
import unittest
import tempfile
from flask_blog.scripts.db import InitDB

class TestRubikBlog(unittest.TestCase):

    def setUp(self):
        self.db_fd, flask_blog.DATABASE = tempfile.mkstemp()
        self.app = flask_blog.app.test_client()
        InitDB().run()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('stiffer', 'aaa')
        assert 'Login Successful!'.encode() in rv.data
        rv = self.logout()
        assert 'Logged Out'.encode() in rv.data
        rv = self.login('admin', 'default')
        assert 'Username is different'.encode() in rv.data
        rv = self.login('stiffer', 'defataultx')
        assert 'Password is different'.encode() in rv.data

if __name__ == '__main__':
    unittest.main()