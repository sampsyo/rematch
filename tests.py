#!venv/bin/python
import os
import unittest

from config import basedir
from server import *
from server.models.professor import Professor

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

    def test_create_student(self): 
        Student.create_student(net_id = "abc",  name = "hello") 
        assert Student.get_student_by_netid("abc") is not None 
        assert len(Student.get_all_students()) == 1
        s1 = Student.create_student(net_id = "abc",  name = "h") 
        assert s1 is None 
        assert len(Student.get_all_students()) == 1 
        s2 = Student.get_student_by_netid("def")
        assert s2 is None
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "hello"
        assert s3.major is None 
        assert s3.year is None 
        assert s3.skills is None 
        assert s3.resume is None 
        assert s3.description is None 
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 

    def test_create_professor(self): 
        Professor.create_professor(net_id = "abc",  name = "hello") 
        assert Professor.get_professor_by_netid("abc") is not None 
        assert len(Professor.get_all_professors()) == 1
        s1 = Professor.create_professor(net_id = "abc",  name = "h") 
        assert s1 is None 
        assert len(Professor.get_all_professors()) == 1 
        s2 = Professor.get_professor_by_netid("def")
        assert s2 is None
        s3 = Professor.get_professor_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.name == "hello"
        assert s3.email == "abc@cornell.edu"
        assert s3.desc is None
        assert s3.interests is None 
 

if __name__ == '__main__':
    unittest.main()
