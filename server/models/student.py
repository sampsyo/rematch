from server import db


class Student(db.Model):
    __tablename__ = 'students'
    net_id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    major = db.Column(db.String(64))
    year = db.Column(db.Integer)
    skills = db.Column(db.String(10000))
    resume = db.Column(db.String(10000))
    description = db.Column(db.String(10000))
    interests = db.Column(db.String(10000))
    favorited_projects = db.Column(db.String(10000))
    availability = db.Column(db.String(10000))

    @classmethod
    def create_student(cls, net_id=net_id, name=name):
        if Student.get_student_by_netid(net_id):
            print("Student already exists with net_id %s" % net_id)
            return None

        student = Student(
            net_id=net_id,
            name=name,
            email=net_id + "@cornell.edu"
        )
        db.steession.add(student) #steession?
        db.session.commit()
        return student

    @classmethod 
    def update_student(cls, net_id, email=None, name=None, major=None, 
        year=None, skills=None, resume=None, description=None, interests=None, 
        favorited_projects=None, availability=None): 
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
        if skills: 
            student.skills = skills
        if resume: 
            studnet.resume = resume
        if description: 
            student.description = description
        if interests: 
            student.interests = interests
        if favorited_projects: 
            student.favorited_projects = favorited_projects 
        if availability: 
            student.availability = availability
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

    @classmethod #returns a list of the favorited projects
    def get_student_favorited_projects_ids(cls, net_id):
        student = Student.get_student_by_netid(net_id)
        if student:
            return student.favorited_projects.split(',')
        else:
            return None

    @classmethod
    def add_favorited_project(cls, net_id, post_id):
        student = Student.get_student_by_netid(net_id)
        if student:
            updated_projects = student.favorited_projects
            if student.favorited_projects == None:
                updated_projects = post_id + ","
            else:
                updated_projects = updated_projects + post_id + ","
            Student.update_student(cls, net_id, favorited_projects = updated_projects)
    
    @classmethod
    def delete_favorited_project(cls, net_id, post_id):
        student = Student.get_student_by_netid(net_id)
        if student:
            if student.favorited_projects != None:
                favorited = student.favorited_projects.split(',')
                if post_id in favorited:
                    favorited.remove(post_id)
                    favorited_string = ""
                    for i in favorited:
                        favorited_string = favorited_string + i + ","
                    Student.update_student(cls, net_id, favorited_projects = favorited_string)


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
            'availability': self.availability
        }
