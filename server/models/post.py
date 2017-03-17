from server import db


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    desc = db.Column(db.String(10000))
    qualifications = db.Column(db.String(10000))
    professor_id = db.Column(db.String(64), db.ForeignKey('professor.net_id'))
    current_students = db.Column(db.String(10000))
    desired_skills = db.Column(db.String(10000))
    capacity = db.Column(db.Integer)
    current_number = db.Column(db.Integer)

    @classmethod
    def create_post(cls, description="", qualifications="", professor_id=""):
        # Gets the new user attempts
        # Converts json into a User instance
        post = Post.create_post(
            description=description,
            qualifications=qualifications,
            professor_id=professor_id,
            current_students="",
            desired_skills="",
            capacity=1,
            current_number=0
        )
        db.session.add(post)
        db.commit()
        return post

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'qualifications': self.qualifications,
            'professor_id': self.professor_id,
            'current_students': self.current_students,
            'desired_skills': self.desired_skills,
            'capacity': self.capacity,
            'current_number': self.current_number
        }
