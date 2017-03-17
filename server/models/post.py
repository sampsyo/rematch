from server import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    desc = db.Column(db.String(10000))
    qualifications = db.Column(db.String(10000))
    professor_id = db.Column(db.String(64), db.ForeignKey('professors.net_id'))
    current_students = db.Column(db.String(10000))
    desired_skills = db.Column(db.String(10000))
    capacity = db.Column(db.Integer)
    current_number = db.Column(db.Integer)

    @classmethod
    def create_post(cls, title="",
                    description="", qualifications="", professor_id=""):
        # Gets the new user attempts
        # Converts json into a User instance
        post = Post.create_post(
            title=title,
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

    @classmethod
    def update_post(cls, post_id, title="", description="", qualifications="",
                    professor_id="", current_students="", desired_skills="",
                    capacity=None, current_number=None):
        post = Post.get_post_by_id(post_id)
        if not post:
            return None
        if title:
            post.title = title
        if description:
            post.description = description
        if qualifications:
            post.qualifications = qualifications
        if professor_id:
            post.professor_id = professor_id
        if current_students:
            post.current_students = current_students
        if desired_skills:
            post.desired_skills = desired_skills
        if capacity:
            post.capacity = int(capacity)
        if current_number:
            post.current_number = int(current_number)
        db.session.commit()
        return post

    @classmethod
    def get_post_by_id(cls, post_id):
        post = Post.query.filter(Post.id == post_id).first()
        if post:
            return post
        else:
            return None

    @classmethod
    def get_posts_by_professor_id(cls, professor_id):
        return [
            p.serialize for p in
            Post.query.filter(Post.professor_id == professor_id).all()
        ]

    @classmethod
    def delete_post(cls, post_id):
        post = Post.get_post_by_id(post_id)
        if post:
            post.delete()
            db.session.commit()
            return True
        else:
            return False

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
