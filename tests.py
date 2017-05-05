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

    def test_create_new_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert Student.get_student_by_netid("abc") is not None 
        assert len(Student.get_all_students()) == 1
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
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_create_student_with_existing_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert Student.get_student_by_netid("abc") is not None 
        assert len(Student.get_all_students()) == 1
        s1 = Student.create_student(net_id = "abc",  name = "h", 
            email = "abc@cornell.edu", password = "123") 
        assert s1 is None 
        assert len(Student.get_all_students()) == 1 

    def test_get_student_with_invalid_netid(self): 
        s2 = Student.get_student_by_netid("def")
        assert s2 is None

    def test_get_all_students_with_empty_database(self): 
        assert len(Student.get_all_students()) == 0
        
    def test_delete_student_with_existing_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        deleted = Student.delete_student("abc")
        assert deleted 
        assert len(Student.get_all_students()) == 0

    def test_delete_student_with_non_existing_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        deleted = Student.delete_student("def")
        assert not deleted 
        assert len(Student.get_all_students()) == 1 
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
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_with_non_existing_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s1 = Student.update_student("def", email="def@cornell.edu")
        assert s1 is None 

    def test_update_student_with_non_existing_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s1 = Student.update_student("def", email="def@cornell.edu")
        assert s1 is None 

    def test_update_student_email(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", "abc@cs.cornell.edu") 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cs.cornell.edu"
        assert s3.name == "hello"
        assert s3.major is None 
        assert s3.year is None 
        assert s3.skills is None 
        assert s3.resume is None 
        assert s3.description is None 
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_name(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", name = "world") 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "world"
        assert s3.major is None 
        assert s3.year is None 
        assert s3.skills is None 
        assert s3.resume is None 
        assert s3.description is None 
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_major(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", major = "computer science") 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "hello"
        assert s3.major == "computer science"
        assert s3.year is None 
        assert s3.skills is None 
        assert s3.resume is None 
        assert s3.description is None 
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_year(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", year = 2018) 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "hello"
        assert s3.major is None 
        assert s3.year == 2018
        assert s3.skills is None 
        assert s3.resume is None 
        assert s3.description is None 
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_skills(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", skills = "skillful") 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "hello"
        assert s3.major is None 
        assert s3.year is None 
        assert s3.skills == "skillful" 
        assert s3.resume is None 
        assert s3.description is None 
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_resume(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", resume = "resume") 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "hello"
        assert s3.major is None 
        assert s3.year is None 
        assert s3.skills is None 
        assert s3.resume == "resume" 
        assert s3.description is None 
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_description(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", description = "description") 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "hello"
        assert s3.major is None 
        assert s3.year is None 
        assert s3.skills is None 
        assert s3.resume is None 
        assert s3.description == "description"
        assert s3.interests is None 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_student_favorited_projects(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", interests = "machine learning") 
        s3 = Student.get_student_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.email == "abc@cornell.edu"
        assert s3.name == "hello"
        assert s3.major is None 
        assert s3.year is None 
        assert s3.skills is None 
        assert s3.resume is None 
        assert s3.description is None
        assert s3.interests == "machine learning" 
        assert s3.favorited_projects is None 
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True  

    def test_update_student_favorited_projects(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", favorited_projects = "project 1") 
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
        assert s3.favorited_projects == "project 1"
        assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True    

    def test_update_student_availability(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", availability = "2018") 
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
        assert s3.availability == "2018" 
        assert s3.courses is None 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True   

    def test_update_student_courses(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", courses = "CS 5150") 
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
        assert s3.courses == "CS 5150" 
        assert s3.is_grad == False 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True     

    def test_update_student_is_grad(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        s3 = Student.update_student("abc", is_grad = True) 
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
        assert s3.courses is None 
        assert s3.is_grad == True 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True      

if __name__ == '__main__':
    unittest.main()
