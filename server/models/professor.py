from server import db


class Professor(db.Model):
    __tablename__ = 'professor'
    net_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='professor', lazy='dynamic')
    desc = db.Column(db.String(10000))
    interests = db.Column(db.String(10000))
#
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
            'email': self.email,
            'posts': self.posts,
            'desc': self.desc,
            'interests': self.interests
        }

#    @property
#    def serialize_posts(self):
#        return [item.serialize for item in self.posts]
#
    def __repr__(self):
        return '<Professor %r>' % (self.name)

