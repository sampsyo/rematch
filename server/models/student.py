from server import db
from post import Post
from werkzeug import generate_password_hash, check_password_hash


class Student(db.Model):
    __tablename__ = 'students'
    net_id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True)
    major = db.Column(db.String(64))
    year = db.Column(db.Integer)
    skills = db.Column(db.String(10000))
    resume = db.Column(db.String(10000))
    description = db.Column(db.String(10000))
    interests = db.Column(db.String(10000))
    favorited_projects = db.Column(db.String(10000))
    courses = db.Column(db.String(10000))
    is_student = True
    is_authenticated = True
    is_active = True
    is_anonymous = True


    """Summary: Returns the current student's net id"""
    def get_id(self):
        return self.net_id


    """Summary: Sets the current student's password
       Parameters:
            password: the password to be set
    """
    def set_password(self, password):
        self.password = generate_password_hash(password)


    """Summary: Returns whether or not password is the student's
                password
       Parameters:
            password: the password to be checked against the 
                      student's password
    """
    def is_correct_password(self, password):
        return check_password_hash(self.password, password)


    """Summary: Creates the current student object using his or 
                her net id, name, email, and password. Returns the
                student object if successfully created
       Parameters:
            net id: the student's net id
            name: the student's name
            email: the student's email
            password: the student's password
    """
    @classmethod
    def create_student(cls, net_id=net_id, name=name, email=email,
                       password=password):
        if Student.get_student_by_netid(net_id):
            return None

        student = Student(
            net_id=net_id,
            name=name,
            email=email,
            password=password,
            major="Computer Science",
            description="",
            courses=""
        )
        db.session.add(student)
        db.session.commit()
        return student


    """Summary: Updates the student object. Only those fields that 
                have been changed update, the rest remain unchanged
       Parameters: 
            net_id: the student's net id
            email: the student's email
            name: the student's name
            major: the student's major
            year: the student's grade
            skills: the student's skills
            resume: the student's resume
            description: a description of the student
            interests: the student's interests
            favorited_projects: the student's favorite projects
            availability: the student's time availability
            courses: the courses the student has taken
    """
    @classmethod
    def update_student(cls, net_id, email=None, name=None, major=None,
                       year=None, skills=None, resume=None, description=None,
                       interests=None, favorited_projects=None,
                       availability=None, courses=None):
        student = Student.get_student_by_netid(net_id)
        if not student:
            return None
        if email:
            student.email = email
        if name:
            student.name = name
        if major:
            student.major = major
        if year:
            student.year = year
        if skills is not None:
            student.skills = skills
        if resume:
            student.resume = resume
        if description:
            student.description = description
        if interests:
            student.interests = interests
        if favorited_projects is not None:
            student.favorited_projects = favorited_projects
        if courses is not None:
            student.courses = courses
        db.session.commit()
        return student


    """Summary: Returns the student object identified by the net_id.
                If no student object has this id, return None.
       Parameters:
            net_id: the net id of the student to return
    """
    @classmethod
    def get_student_by_netid(cls, net_id):
        student = Student.query.filter(Student.net_id == net_id).first()
        if student:
            return student
        else:
            return None


    """Summary: returns all student objects in the database"""
    @classmethod
    def get_all_students(cls):
        return [s.serialize for s in Student.query.all()]


    """Summary: Deletes the student object identified by net_id from the 
                database and return True. If no student object has this id, 
                delete nothing and return False
       Parameters: 
            net_id: the net id of the student object to delete
    """
    @classmethod
    def delete_student(cls, net_id):
        student = Student.get_student_by_netid(net_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        else:
            return False


    """Summary: Returns a student's favorited projects based on their net id
       Parameters:
            net_id: the net id of the student for which to return hir or her
                    favorited projects
    """
    @classmethod 
    def get_student_favorited_projects(cls, net_id):
        student = Student.get_student_by_netid(net_id)
        posts = []
        if student:
            if student.favorited_projects is not None:
                for p in student.favorited_projects.split(','):
                    post_obj = Post.get_post_by_id(p)
                    if post_obj:
                        posts.append(post_obj.serialize_compressed_post)
            return posts

        else:
            return None


    """Summary: Add a projects to a student's favorited list
       Parameters:
            net_id: the net id of the student to add the 
                    favorited project to
            post_id: the id of the post to add to the student's
                     favorited projects list
    """
    @classmethod
    def add_favorited_project(cls, net_id, post_id):
        student = Student.get_student_by_netid(net_id)
        post = Post.get_post_by_id(post_id)
        if student and post:

            favorites = set()
            if student.favorited_projects:
                favorites = set(student.favorited_projects.split(','))

            favorites.add(str(post_id))
            new_favorites = ",".join(favorites)
            Student.update_student(net_id, favorited_projects=new_favorites)
            return True


    """Summary: Delete a projects from a student's favorited list
       Parameters:
            net_id: the net id of the student to delete the 
                    favorited project from
            post_id: the id of the post to delete from the student's
                     favorited projects list
    """ 
    @classmethod
    def delete_favorited_project(cls, net_id, post_id):
        student = Student.get_student_by_netid(net_id)
        if student:
            if student.favorited_projects is not None:
                new_favorites = ",".join(
                    pid for pid in student.favorited_projects.split(',')
                    if not pid == str(post_id)
                )
                Student.update_student(net_id,
                                       favorited_projects=new_favorites)
                return True
            else:
                return False

    def __init__(self, password, **kwargs):
        super(Student, self).__init__(**kwargs)
        self.set_password(password)


    """Summary: returns a student object as a dictionary that can be turned 
    into a json"""
    @property
    def serialize(self):
        return {
            'net_id': self.net_id,
            'name': self.name,
            'major': self.major,
            'year': self.year,
            'skills': self.skills,
            'resume': self.resume,
            'description': self.description,
            'interests': self.interests,
            'favorited_projects': self.favorited_projects,
            'courses': self.courses or ''
        }
