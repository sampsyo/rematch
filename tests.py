#!venv/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Post

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_posts(self):
        u1 = User(email ='blah', name='john')
        u2 = User(email ='zed', name='badGuy')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.posts.count() is 0
        assert u2.posts.count() is 0 
        p1 = Post( post='Hi! This is my first post')
        assert p1.user_id is None
        u1.create_post(p1)
        db.session.add(p1)
        db.session.commit()
        assert p1.user_id is not None
        assert u2.create_post(p1) is None
        assert u1.posts.count() is not 0
        print(u1.posts.first().post)
        assert u1.posts.first().user_id == u1.id
        u1.delete_post(p1)
        assert u1.posts.count() is 0




if __name__ == '__main__':
    unittest.main()
