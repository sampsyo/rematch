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

    def test_create_post(self): 
        Professor.create_professor(net_id = "aish",  name = "aish") 
        p1 = Post.create_post(title="hello", description="world", 
            qualifications="bye", professor_id="world")
        assert p1 is None 
        p2 = Post.create_post(title="hello", description="world", 
            qualifications="bye", professor_id="aish")
        assert p2.title == "hello" 
        assert p2.description == "world"
        assert p2.qualifications == "bye"
        assert p2.professor_id == "aish"
        assert p2.desc is None 
        assert p2.current_students is None 
        assert p2.desired_skills is None 
        assert p2.capacity is None 
        assert p2.current_number is None 
        assert len(Post.get_all_posts) == 1
        assert len(Post.get_posts_by_professor_id("aish")) == 1   

    def test_update_post(self): 
        Professor.create_professor(net_id = "aish",  name = "aish") 
        p2 = Post.create_post(title="hello", description="world", 
            qualifications="bye", professor_id="aish")
        Post.update_post(post_id = p2.id, desired_skills = "CS")
        Post.update_post(post_id = p2.id, capacity = 5)
        assert p2.title == "hello" 
        assert p2.description == "world"
        assert p2.qualifications == "bye"
        assert p2.professor_id == "aish"
        assert p2.desc is None 
        assert p2.current_students is None 
        assert p2.desired_skills == "CS"
        assert p2.capacity == 5 
        assert p2.current_number is None 
        assert len(Post.get_all_posts) == 1
        assert len(Post.get_posts_by_professor_id("aish")) == 1    

    def test_delete_post(self): 
        Professor.create_professor(net_id = "aish",  name = "aish") 
        p2 = Post.create_post(title="hello", description="world", 
            qualifications="bye", professor_id="aish")   
        deleted = Post.delete_post(p2.id) 
        assert deleted 
        assert len(Post.get_all_posts) == 0
        assert len(Post.get_posts_by_professor_id("aish")) == 0  

if __name__ == '__main__':
    unittest.main()
