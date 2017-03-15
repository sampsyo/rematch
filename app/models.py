from app import db

# TODO: Search not currently enabled , can lookup but not search. 
# Searching with whoosh is dif with version Python 3 > so only enable if less!
# import sys
# if sys.version_info >= (3, 0):
#   enable_search = False
# else:
#   enable_search = True
#   import flask_whooshalchemy as whooshalchemy


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')


    #Post Helper Funcs
    #Posts had unique creator and cannot be added twice to a user
    def create_post(self, post):
        if post.user_id is None:
            if not self.has_post(post):
                self.posts.append(post)
                return self
        else:
            print("This post is already affiliated with a user")
            

    def delete_post(self, post):
        if self.has_post(post):
            self.posts.remove(post)
            return self

    def has_post(self, post):
        return self.posts.filter(Post.id==post.id).count() > 0  

    #This is to convert calls for User into json friendly format!
    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'posts' : self.serialize_posts
        }

    @property
    def serialize_posts(self):
        return [ item.serialize for item in self.posts ]

    def __repr__(self):
        return '<User %r>' % (self.name)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'post' : self.post,
            'user_id' : self.user_id
        }
        