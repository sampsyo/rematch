#!venv/bin/python
import os
import unittest

import datetime
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

    def test_get_student_id(self): 
        s1 = Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert s1.get_id() == "abc"

    def test_student_is_correct_password_with_correct_password(self): 
        s1 = Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert s1.is_correct_password("123")

    def test_student_is_correct_password_with_incorrect_password(self): 
        s1 = Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert not s1.is_correct_password("456")

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
        s3 = Student.update_student("abc", email = "abc@cs.cornell.edu") 
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

    def test_get_student_with_invalid_netid(self): 
        s2 = Student.get_student_by_netid("def")
        assert s2 is None

    def test_get_student_with_valid_netid(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        s3 = Student.get_student_by_netid("abc")
        assert s3 is not None 
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

    def test_get_all_students_with_empty_database(self): 
        assert len(Student.get_all_students()) == 0

    def test_get_all_students_with_one_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        s = Student.get_all_students() 
        assert len(s) == 1
        assert s[0]["net_id"] == "abc"

    def test_get_all_students_with_multiple_students(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        Student.create_student(net_id = "def",  name = "hello2", 
            email = "def@cornell.edu", password = "123") 
        Student.create_student(net_id = "ghi",  name = "hello3", 
            email = "ghi@cornell.edu", password = "123") 
        s = Student.get_all_students() 
        assert len(s) == 3
        assert s[0]["net_id"] == "abc"
        assert s[1]["net_id"] == "def"
        assert s[2]["net_id"] == "ghi"
        
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

    def test_get_student_favorited_projects_for_non_existing_student(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        l1 = Student.get_student_favorited_projects("def") 
        assert l1 is None 

    def test_get_student_favorited_projects_with_zero_favorited_project(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1 
        l1 = Student.get_student_favorited_projects("abc") 
        assert l1 == []

    def test_get_student_favorited_projects_with_one_favorited_project(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        Professor.create_professor("def", "prof", "def@cornell.edu", "456") 
        assert len(Professor.get_all_professors()) == 1
        assert len(Student.get_all_students()) == 1 
        p1 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        assert p1.id == 1
        Student.update_student("abc", favorited_projects = "1")
        l1 = Student.get_student_favorited_projects("abc") 
        assert len(l1) == 1
        assert l1[0]["id"] == 1

    def test_get_student_favorited_projects_with_multiple_favorited_project(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        Professor.create_professor("def", "prof", "def@cornell.edu", "456") 
        assert len(Professor.get_all_professors()) == 1
        assert len(Student.get_all_students()) == 1 
        p1 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        p2 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        p3 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        assert p1.id == 1
        assert p2.id == 2
        assert p3.id == 3
        Student.update_student("abc", favorited_projects = "1,2,3")
        l1 = Student.get_student_favorited_projects("abc") 
        assert len(l1) == 3
        assert l1[0]["id"] == 1
        assert l1[1]["id"] == 2
        assert l1[2]["id"] == 3

    def test_delete_favorited_projects_with_invalid_netid(self): 
        p1 = Student.delete_favorited_project("def", "1") 
        assert p1 is None 

    def test_delete_favorited_projects_with_valid_netid_and_no_project(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Student.get_all_students()) == 1
        b1 = Student.delete_favorited_project("abc", "1")
        assert not b1 

    def test_delete_favorited_projects_with_one_correct_favorited_project(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        Professor.create_professor("def", "prof", "def@cornell.edu", "456") 
        assert len(Professor.get_all_professors()) == 1
        assert len(Student.get_all_students()) == 1 
        p1 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        assert p1.id == 1
        Student.update_student("abc", favorited_projects = "1")
        l1 = Student.delete_favorited_project("abc", "1") 
        assert l1 
        assert Student.get_student_by_netid("abc").favorited_projects == "" 

    def test_delete_favorited_projects_with_one_wrong_favorited_project(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        Professor.create_professor("def", "prof", "def@cornell.edu", "456") 
        assert len(Professor.get_all_professors()) == 1
        assert len(Student.get_all_students()) == 1 
        p1 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        assert p1.id == 1
        Student.update_student("abc", favorited_projects = "1")
        l1 = Student.delete_favorited_project("abc", "2") 
        assert l1 
        assert Student.get_student_by_netid("abc").favorited_projects == "1" 

    def test_delete_favorited_projects_with_multiple_projects(self): 
        Student.create_student(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        Professor.create_professor("def", "prof", "def@cornell.edu", "456") 
        assert len(Professor.get_all_professors()) == 1
        assert len(Student.get_all_students()) == 1 
        p1 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        p2 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        p3 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "required_courses", False)
        assert p1.id == 1
        assert p2.id == 2
        assert p3.id == 3
        Student.update_student("abc", favorited_projects = "1,2,3")
        l1 = Student.delete_favorited_project("abc", "2") 
        assert l1 
        assert Student.get_student_by_netid("abc").favorited_projects == "1,3" 

    def test_get_professor_id(self): 
        s1 = Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert s1.get_id() == "abc"

    def test_professor_is_correct_password_with_correct_password(self): 
        s1 = Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert s1.is_correct_password("123")

    def test_professor_is_correct_password_with_incorrect_password(self): 
        s1 = Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert not s1.is_correct_password("456")

    def test_create_new_professor(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert Professor.get_professor_by_netid("abc") is not None 
        assert len(Professor.get_all_professors()) == 1
        s3 = Professor.get_professor_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.name == "hello"
        assert s3.email == "abc@cornell.edu"
        assert s3.password == "123"
        assert s3.desc is None
        assert s3.interests is None 
        assert s3.is_student == False 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_create_professor_with_existing_professor(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert Professor.get_professor_by_netid("abc") is not None 
        assert len(Professor.get_all_professors()) == 1
        s1 = Professor.create_professor(net_id = "abc",  name = "h", 
            email = "abc@cornell.edu", password = "123")         
        assert s1 is None 
        assert len(Professor.get_all_professors()) == 1 

    def test_update_professor_with_none_existing_professor(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Professor.get_all_professors()) == 1 
        s1 = Professor.update_professor("def", email="def@cornell.edu")
        assert s1 is None 

    def test_update_professor_email(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Professor.get_all_professors()) == 1 
        s3 = Professor.update_professor("abc", email = "abc@cs.cornell.edu") 
        s3 = Professor.get_professor_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.name == "hello"
        assert s3.email == "abc@cs.cornell.edu"
        assert s3.password == "123"
        assert s3.desc is None
        assert s3.interests is None 
        assert s3.is_student == False 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_professor_name(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Professor.get_all_professors()) == 1 
        s3 = Professor.update_professor("abc", name="world") 
        s3 = Professor.get_professor_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.name == "world"
        assert s3.email == "abc@cornell.edu"
        assert s3.password == "123"
        assert s3.desc is None
        assert s3.interests is None 
        assert s3.is_student == False 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_professor_desc(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Professor.get_all_professors()) == 1 
        s3 = Professor.update_professor("abc", desc = "new description") 
        s3 = Professor.get_professor_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.name == "hello"
        assert s3.email == "abc@cornell.edu"
        assert s3.password == "123"
        assert s3.desc == "new description"
        assert s3.interests is None 
        assert s3.is_student == False 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_update_professor_interests(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        assert len(Professor.get_all_professors()) == 1 
        s3 = Professor.update_professor("abc", interests = "new interests") 
        s3 = Professor.get_professor_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.name == "hello"
        assert s3.email == "abc@cornell.edu"
        assert s3.password == "123"
        assert s3.desc is None
        assert s3.interests == "new interests"
        assert s3.is_student == False 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_get_professor_with_invalid_netid(self): 
        s2 = Professor.get_professor_by_netid("def")
        assert s2 is None

    def test_get_professor_with_valid_netid(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        s3 = Professor.get_professor_by_netid("abc") 
        assert s3.net_id == "abc"
        assert s3.name == "hello"
        assert s3.email == "abc@cornell.edu"
        assert s3.password == "123"
        assert s3.desc is None
        assert s3.interests is None 
        assert s3.is_student == False 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True 

    def test_get_all_professors_with_empty_database(self): 
        assert len(Professor.get_all_professors()) == 0

    def test_get_all_professors_with_one_professor(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        s = Professor.get_all_professors() 
        assert len(s) == 1
        assert s[0]["net_id"] == "abc"

    def test_get_all_professors_with_multiple_professors(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        Professor.create_professor(net_id = "def",  name = "hello2", 
            email = "def@cornell.edu", password = "123") 
        Professor.create_professor(net_id = "ghi",  name = "hello3", 
            email = "ghi@cornell.edu", password = "123") 
        s = Professor.get_all_professors() 
        assert len(s) == 3
        assert s[0]["net_id"] == "abc"
        assert s[1]["net_id"] == "def"
        assert s[2]["net_id"] == "ghi"

if __name__ == '__main__':
    unittest.main()
