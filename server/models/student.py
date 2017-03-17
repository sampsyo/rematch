from server import db


class Student(db.Model):
    __tablename__ = 'students'
    net_id = db.Column(db.String(64), primary_key=True)
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
            name=name
        )
        db.session.add(student)
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

#    # Post Helper Funcs
#    # Posts had unique creator and cannot be added twice to a user
#    def create_post(self, post):
#        if post.user_id is None:
#            if not self.has_post(post):
#                self.posts.append(post)
#                return self
#        else:
#            print("This post is already affiliated with a user")
#
#    def delete_post(self, post):
#        if self.has_post(post):
#            self.posts.remove(post)
#            return self
#
#    def has_post(self, post):
#        return self.posts.filter(Post.id == post.id).count() > 0

    # This is to convert calls for User into json friendly format!
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

#    @property
#    def serialize_posts(self):
#        return [item.serialize for item in self.posts]
#
