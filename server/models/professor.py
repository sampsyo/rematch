from server import db


class Professor(db.Model):
    __tablename__ = 'professors'
    net_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    desc = db.Column(db.String(10000))
    interests = db.Column(db.String(10000))

    # This is to convert calls for User into json friendly format!
    @property
    def serialize(self):
        return {
            'net_id': self.net_id,
            'name': self.name,
            'email': self.email,
            'posts': self.posts,
            'desc': self.desc,
            'interests': self.interests
        }
