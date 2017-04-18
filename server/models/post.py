import datetime
from server import db
# from server.models.professor import Professor


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(10000))
    professor_id = db.Column(db.String(64), db.ForeignKey('professors.net_id'))
    tags = db.Column(db.String(10000))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    stale_date = db.Column(db.DateTime)

    # unimplemented
    qualifications = db.Column(db.String(10000))
    current_students = db.Column(db.String(10000))
    desired_skills = db.Column(db.String(10000))
    capacity = db.Column(db.Integer)
    current_number = db.Column(db.Integer)

    def is_stale(self):
        return self.stale_date is not None and self.stale_date < datetime.now()

    @classmethod
    def refresh(cls, post_id, days_added):
        post = Post.get_post_by_id(post_id)
        if post.stale_date:
            post.stale_date += datetime.timedelta(days=days_added)

    @classmethod
    def get_posts(cls, tags=None, exclusive=False):
        """ Gets posts in the database.  If a list of tags is supplied, filters
        based on those tags.  If exclusive is set True, then post must have
        all tags applied, else post must have at least one tag applied. """
        if not tags:
            return [p.serialize for p in Post.query.all()]

        # TODO inefficiency: currently must pull all posts, then filter,
        # because tags cannot be searched through SQLLite
        if exclusive:
            return [
                p.serialize for p in Post.query.all() if
                set(tags).issubset(set(p.serialize['tags']))
            ]
        else:
            return [
                p.serialize for p in Post.query.all() if
                len(set(tags).intersection(set(p.serialize['tags']))) > 0
            ]

    @classmethod
    def get_compressed_posts(cls, tags=None, exclusive=False):
        """ Gets posts in the database.  If a list of tags is supplied, filters
        based on those tags.  If exclusive is set True, then post must have
        all tags applied, else post must have at least one tag applied. """
        if not tags:
            return [p.serialize_compressed_post for p in Post.query.all()]

        # TODO inefficiency: currently must pull all posts, then filter,
        # because tags cannot be searched through SQLLite
        if exclusive:
            return [
                p.serialize_compressed_post for p in Post.query.all() if
                set(tags).issubset(set(p.serialize_compressed_post['tags']))
            ]
        else:
            return [
                p.serialize_compressed_post for p in Post.query.all() if
                len(set(tags).intersection(
                    set(p.serialize_compressed_post['tags'])
                )) > 0
            ]

    @classmethod
    def create_post(cls, title, description, professor_id, tags,
                    qualifications, desired_skills, stale_days):
        # if not (Professor.get_professor_by_netid(professor_id)):
        #    return None
        stale_date = None
        if stale_days:
            stale_date = datetime.now() + datetime.timedelta(days=stale_days)

        post = Post(
            title=title,
            description=description,
            tags=",".join(tags),
            professor_id=professor_id,
            qualifications=qualifications,
            desired_skills="",
            stale_date=stale_date
        )
        db.session.add(post)
        db.session.commit()
        return post

    # Keep arguments in alphabetical order!
    @classmethod
    def update_post(cls, post_id,
                    description=None, desired_skills=None, is_active=None,
                    professor_id=None, qualifications=None, tags=None,
                    title=None):
        post = Post.get_post_by_id(post_id)
        if not post:
            return None
        if title:
            post.title = title
        if description:
            post.description = description
        if tags:
            post.tags = ",".join(tags)
        if qualifications:
            post.qualifications = qualifications
        if professor_id:
            post.professor_id = professor_id
        if desired_skills:
            post.desired_skills = desired_skills
        if is_active is not None:
            post.is_active = is_active
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
            db.session.delete(post)
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def mark_post_complete(cls, post_id):
        post = Post.get_post_by_id(post_id)
        if not post:
            return False

        cls.update_post(cls, post_id, is_active=False)
        db.session.commit()
        return True

    @classmethod
    def get_all_active_posts(cls):
        return [s.serialize for s in Post.query.filter_by(is_active=True).all()]

    @classmethod
    def get_all_stale_posts(cls):
        return [
            s.serialize for s in Post.query.filter_by(is_active=False).all()
        ]

    #may be broken
    @classmethod
    def get_posts_by_keywords(cls, keywords):
        posts = []
        for p in Post.query.filter_by(is_active=True).all():
            for keyword in keywords: #check if its actually gonna be a list
                if (keyword in p.title) or (keyword in p.description) \
                    or (keyword in p.tags) or (keyword in p.professor_id) \
                    or (keyword in p.desired_skills):
                    posts.append(p.serialize_compressed_post)
        return posts

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags.split(','),
            'qualifications': self.qualifications,
            'professor_id': self.professor_id,
            'desired_skills': self.desired_skills,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'stale_date': self.stale_date
        }

    @property
    def serialize_compressed_post(self):
        return {
            'id': self.id,
            'title': self.title,
            # only 150 words
            'description': (
                " ".join(self.description.split(" ")[:75]) + '...'
                if len(self.description.split(" ")) > 75 else self.description),
            # only 5 tags
            'tags': self.tags.split(',')[:5],
            'professor_id': self.professor_id,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }
