from server import db
from post import Post


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
    #availability = db.Column(db.String(10000))
    courses = db.Column(db.String(10000))
    #is_grad = db.Column(db.Boolean, default = False)
    is_student = True

    # This is for Login Stuff
    is_authenticated = True
    is_active = True
    is_anonymous = True

    def get_id(self):
        return self.net_id

    def is_correct_password(self, password):
        return self.password == password

    @classmethod
    def create_student(
        cls, net_id=net_id, name=name, email=email, password=password
    ):
        if Student.get_student_by_netid(net_id):
            return None

        student = Student(
            net_id=net_id,
            name=name,
            email=email,
            password=password  # Just for NOW!!
        )
        db.session.add(student)
        db.session.commit()
        return student

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
        #if availability:
        #    student.availability = availability
        if courses is not None: 
            student.courses = courses
        #if is_grad is not None:
        #    student.is_grad = is_grad
        db.session.commit()
        return student

    @classmethod
    def get_student_by_netid(cls, net_id):
        student = Student.query.filter(Student.net_id == net_id).first()
        if student:
            return student
        else:
            return None

    @classmethod
    def get_all_students(cls):
        return [s.serialize for s in Student.query.all()]

    @classmethod
    def delete_student(cls, net_id):
        student = Student.get_student_by_netid(net_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        else:
            return False

    # can this just return the posts objects?
    # or is it better to do that in the routes?

    @classmethod  # returns a list of the favorited projects
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

    @classmethod
    def delete_favorited_project(cls, net_id, post_id):
        student = Student.get_student_by_netid(net_id)
        if student:
            if student.favorited_projects is not None:
                new_favorites = ",".join(
                    pid for pid in student.favorited_projects.split(',')
                    if not pid == str(post_id)
                )
                Student.update_student(net_id, favorited_projects=new_favorites)
                return True
            else: 
                return False 

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
            #'availability': self.availability,
            'courses': self.courses
            #'is_grad': self.is_grad
        }
