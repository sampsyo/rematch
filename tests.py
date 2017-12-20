#!venv/bin/python
import os
import unittest

import datetime
from server import *
from server.models.professor import Professor

basedir = os.path.abspath(os.path.dirname(__file__))

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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
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
        # assert s3.availability is None 
        assert s3.courses is None 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True   

    # def test_update_student_availability(self): 
    #     Student.create_student(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123") 
    #     assert len(Student.get_all_students()) == 1 
    #     s3 = Student.update_student("abc", availability = "2018") 
    #     s3 = Student.get_student_by_netid("abc") 
    #     assert s3.net_id == "abc"
    #     assert s3.email == "abc@cornell.edu"
    #     assert s3.name == "hello"
    #     assert s3.major is None 
    #     assert s3.year is None 
    #     assert s3.skills is None 
    #     assert s3.resume is None 
    #     assert s3.description is None
    #     assert s3.interests is None 
    #     assert s3.favorited_projects is None 
    #     assert s3.availability == "2018" 
    #     assert s3.courses is None 
    #     assert s3.grad_only == False 
    #     assert s3.is_student == True 
    #     assert s3.is_authenticated == True 
    #     assert s3.is_active == True 
    #     assert s3.is_anonymous == True   

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
        # assert s3.availability is None 
        assert s3.courses == "CS 5150" 
        assert s3.is_student == True 
        assert s3.is_authenticated == True 
        assert s3.is_active == True 
        assert s3.is_anonymous == True     

    # def test_update_student_grad_only(self): 
    #     Student.create_student(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123") 
    #     assert len(Student.get_all_students()) == 1 
    #     s3 = Student.update_student("abc", grad_only = True) 
    #     s3 = Student.get_student_by_netid("abc") 
    #     assert s3.net_id == "abc"
    #     assert s3.email == "abc@cornell.edu"
    #     assert s3.name == "hello"
    #     assert s3.major is None 
    #     assert s3.year is None 
    #     assert s3.skills is None 
    #     assert s3.resume is None 
    #     assert s3.description is None
    #     assert s3.interests is None 
    #     assert s3.favorited_projects is None 
        # # assert s3.availability is None 
        # assert s3.courses is None 
        # assert s3.grad_only == True 
        # assert s3.is_student == True 
        # assert s3.is_authenticated == True 
        # assert s3.is_active == True 
        # assert s3.is_anonymous == True     

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
        # assert s3.availability is None 
        assert s3.courses is None 
        # assert s3.grad_only == False 
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
        # assert s3.availability is None 
        assert s3.courses is None 
        # assert s3.grad_only == False 
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
            "project_link", "courses")
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
            "project_link", "courses")
        p2 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "courses")
        p3 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "courses")
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
            "project_link", "courses")
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
            "project_link", "courses")
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
            "project_link", "courses")
        p2 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "courses")
        p3 = Post.create_post("title", "description", "def", "tags", 
            "qualifications", "desired_skills", None, "contact_email", 
            "project_link", "courses")
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
        s3 = Professor.update_professor("abc", website = "new description") 
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
        s3 = Professor.update_professor("abc", office = "new interests") 
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

    def test_is_stale_with_active_post(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123")        
        p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        b = p1.is_stale()
        assert not b 

    # def test_is_stale_with_inactive_post(self): 
    #     Professor.create_professor(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123")        
    #     p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
    #         "desired_skills", 1, "contact_email", "project_link", 
    #         "courses")
    #     b = p1.is_stale()
    #     assert not b 
    #     Post.refresh(1, -1)
    #     p2 = Post.get_post_by_id(1) 
    #     b2 = p2.is_stale()
    #     assert b2

    # def test_refresh_with_0_days(self): 
    #     Professor.create_professor(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123")        
    #     p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
    #         "desired_skills", None, "contact_email", "project_link", 
    #         "courses")
    #     Post.refresh(1, 0)
    #     p2 = Post.get_post_by_id(1) 
    #     assert p1.stale_date == p2.stale_date

    # def test_refresh_with_positive_days(self): 
    #     Professor.create_professor(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123")        
    #     p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
    #         "desired_skills", None, "contact_email", "project_link", 
    #         "courses")
    #     t1 = p1.stale_date
    #     Post.refresh(1, 5)
    #     p2 = Post.get_post_by_id(1) 
    #     assert t1 + datetime.timedelta(days=5) == p2.stale_date

    # def test_refresh_with_negative_days(self): 
    #     Professor.create_professor(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123")        
    #     p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
    #         "desired_skills", None, "contact_email", "project_link", 
    #         "courses")
    #     t1 = p1.stale_date
    #     Post.refresh(1, -5)
    #     p2 = Post.get_post_by_id(1) 
    #     assert t1 == p2.stale_date + datetime.timedelta(days=5) 

    def test_get_posts_with_zero_post(self): 
        l = Post.get_posts()
        assert l[0] == []
        assert l[1] is None  

    def test_get_posts_with_one_post(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123")        
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created 
        t2 = p1.date_modified 
        t3 = p1.stale_date
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["date_modified"] == t2 
        assert post["stale_date"] is None 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_get_posts_with_multiple_posts(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123")        
        p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p3 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l = Post.get_posts()[0]
        assert len(l) == 3
        assert l[0]["id"] == 3
        assert l[1]["id"] == 2
        assert l[2]["id"] == 1

    def test_get_posts_with_pagination_one_page(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123")        
        p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l1 = Post.get_posts(page = 1)[0]
        assert len(l1) == app.config['PAGINATION_PER_PAGE']

    def test_get_posts_with_pagination_two_pages(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123")        
        p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p3 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l1 = Post.get_posts(page = 1)[0]
        assert len(l1) == 2
        l2 = Post.get_posts(page = 2)[0]
        assert len(l2) == 1

    def test_get_posts_from_professor_who_has_no_posts(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123")   
        l = Post.get_posts(professor_id = "1") 
        assert l[0] == [] 
        assert l[1] is None

    def test_get_posts_from_professor_who_has_one_post(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        l = Post.get_posts(professor_id = "1")[0]
        assert len(l) == 1
        post = l[0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["date_modified"] == t2 
        assert post["stale_date"] is t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_get_posts_from_professor_who_has_multiple_posts(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p3 = Post.create_post("title", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l = Post.get_posts(professor_id = "1")[0]
        assert len(l) == 3
        assert l[0]["id"] == 3
        assert l[1]["id"] == 2
        assert l[2]["id"] == 1

    def test_get_posts_with_matching_keywords(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title1", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title2", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p3 = Post.create_post("title3", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l = Post.get_posts(keywords = "title")[0]
        assert len(l) == 3
        assert l[0]["id"] == 3
        assert l[1]["id"] == 2
        assert l[2]["id"] == 1

    def test_get_posts_with_no_matching_keywords(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title1", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title2", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p3 = Post.create_post("title3", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l = Post.get_posts(keywords = "sfkjd")[0]
        assert l == []

    def test_get_posts_with_matching_tags(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title1", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title2", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p3 = Post.create_post("title3", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l = Post.get_posts(tags = 't,g')[0]
        assert len(l) == 3
        assert l[0]["id"] == 3
        assert l[1]["id"] == 2
        assert l[2]["id"] == 1   

    def test_get_posts_with_no_matching_tags(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title1", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p2 = Post.create_post("title2", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        p3 = Post.create_post("title3", "description", "1", "tags", "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        l = Post.get_posts(tags = 'e')[0]
        assert len(l) == 0 

    def test_create_post(self):     
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created 
        t2 = p1.date_modified 
        t3 = p1.stale_date
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["date_modified"] == t2 
        assert post["stale_date"] is None 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_with_non_existing_post(self): 
        p = Post.update_post(1)
        assert p is None 

    def test_update_post_description(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, description = "new description")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "new description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_desired_skills(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, desired_skills = "new desired_skills")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "new desired_skills"

    def test_update_post_is_active(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, is_active = False)
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert not post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_professor_id(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, professor_id = "2")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "2"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_qualifications(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, qualifications = "new qualifications")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "new qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_courses(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, required_courses = "new required courses")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["new required courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_tags(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, tags = ["tag1", "tag2"])
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tag1", "tag2"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_title(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, title = "new title")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "new title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_project_link(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, project_link = "new project_link")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "new project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_update_post_contact_email(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.update_post(1, contact_email = "new contact_email")
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "description"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "new contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    # def test_update_tags_from_desc_with_no_keyword(self): 
    #     Professor.create_professor(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123") 
    #     p1 = Post.create_post("title", "description", "1", ["tags"], "qualifications", 
    #         "desired_skills", 1, "contact_email", "project_link", 
    #         "courses")
    #     t1 = p1.date_created
    #     t2 = p1.date_modified
    #     t3 = p1.stale_date
    #     Post.update_tags_from_desc(p1)
    #     l = Post.get_posts()
    #     assert len(l[0]) == 1
    #     post = l[0][0]
    #     assert post["id"] == 1 
    #     assert post["title"] == "title"
    #     assert post["description"] == "description"
    #     assert post["professor_id"] == "1"
    #     assert post["tags"] == ["tags", "c"]
    #     assert post["is_active"]
    #     assert post["date_created"] == t1 
    #     assert post["date_modified"] == t2 
    #     assert post["stale_date"] == t3 
    #     assert post["contact_email"] == "contact_email"
    #     assert post["project_link"] == "project_link"
    #     assert post["courses"] == "courses"
    #     assert post["qualifications"] == "qualifications"
    #     assert post["desired_skills"] == "desired_skills"

    # def test_update_tags_from_desc_with_keywords(self): 
    #     Professor.create_professor(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123") 
    #     p1 = Post.create_post("title", "machine learning algorithms java", 
    #         "1", ["tags"], "qualifications", 
    #         "desired_skills", 1, "contact_email", "project_link", 
    #         "courses")
    #     t1 = p1.date_created
    #     t2 = p1.date_modified
    #     t3 = p1.stale_date
    #     Post.update_tags_from_desc(p1)
    #     l = Post.get_posts()
    #     assert len(l[0]) == 1
    #     post = l[0][0]
    #     assert post["id"] == 1 
    #     assert post["title"] == "title"
    #     assert post["description"] == "machine learning algorithms java"
    #     assert post["professor_id"] == "1"
    #     assert post["tags"] == ["tags", "algorithms", "machine learning", "java", "c"]
    #     assert post["is_active"]
    #     assert post["date_created"] == t1 
    #     assert post["date_modified"] == t2 
    #     assert post["stale_date"] == t3 
    #     assert post["contact_email"] == "contact_email"
    #     assert post["project_link"] == "project_link"
    #     assert post["courses"] == "courses"
    #     assert post["qualifications"] == "qualifications"
    #     assert post["desired_skills"] == "desired_skills"

    def test_get_post_by_id_with_invalid_id(self): 
        p = Post.get_post_by_id(1)
        assert p is None 

    def test_get_post_by_id_with_valid_id(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "machine learning algorithms java", 
            "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        t1 = p1.date_created
        t2 = p1.date_modified
        t3 = p1.stale_date
        Post.get_post_by_id(1)
        l = Post.get_posts()
        assert len(l[0]) == 1
        post = l[0][0]
        assert post["id"] == 1 
        assert post["title"] == "title"
        assert post["description"] == "machine learning algorithms java"
        assert post["professor_id"] == "1"
        assert post["tags"] == ["tags"]
        assert post["is_active"]
        assert post["date_created"] == t1 
        assert post["date_modified"] == t2 
        assert post["stale_date"] == t3 
        assert post["contact_email"] == "contact_email"
        assert post["project_link"] == "project_link"
        assert post["courses"] == ["courses"]
        assert post["qualifications"] == "qualifications"
        assert post["desired_skills"] == "desired_skills"

    def test_delete_post_with_invalid_post_id(self): 
        post = Post.delete_post(1)
        assert not post

    def test_delete_post_with_valid_post_id(self): 
        Professor.create_professor(net_id = "abc",  name = "hello", 
            email = "abc@cornell.edu", password = "123") 
        p1 = Post.create_post("title", "machine learning algorithms java", 
            "1", ["tags"], "qualifications", 
            "desired_skills", None, "contact_email", "project_link", 
            "courses")
        Post.delete_post(1)
        post = Post.get_post_by_id(1)
        assert not post 

    # def test_mark_post_complete_with_invalid_post_id(self): 
    #     post = Post.mark_post_complete(1)
    #     assert not post 

    # def test_mark_post_complete_with_valid_post_id(self): 
    #     Professor.create_professor(net_id = "abc",  name = "hello", 
    #         email = "abc@cornell.edu", password = "123") 
    #     p1 = Post.create_post("title", "machine learning algorithms java", 
    #         "1", ["tags"], "qualifications", 
    #         "desired_skills", 1, "contact_email", "project_link", 
    #         "courses")
    #     t1 = p1.date_created
    #     t2 = p1.date_modified
    #     t3 = p1.stale_date
    #     b = Post.mark_post_complete(1)
    #     assert b 
    #     l = Post.get_posts()
    #     assert len(l[0]) == 1
    #     post = l[0][0]
    #     assert post["id"] == 1 
    #     assert post["title"] == "title"
    #     assert post["description"] == "machine learning algorithms java"
    #     assert post["professor_id"] == "1"
    #     assert post["tags"] == ["tags"]
    #     assert not post["is_active"]
    #     assert post["date_created"] == t1 
    #     assert post["stale_date"] == t3 
    #     assert post["contact_email"] == "contact_email"
    #     assert post["project_link"] == "project_link"
    #     assert post["courses"] == "courses"
    #     assert post["qualifications"] == "qualifications"
    #     assert post["desired_skills"] == "desired_skills"

if __name__ == '__main__':
    unittest.main()
