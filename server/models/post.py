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

    # unimplemented
    qualifications = db.Column(db.String(10000))
    current_students = db.Column(db.String(10000))
    desired_skills = db.Column(db.String(10000))
    capacity = db.Column(db.Integer)
    current_number = db.Column(db.Integer)

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
    def create_post(cls, title, description, professor_id, tags,
                    qualifications, current_students, desired_skills,
                    capacity, current_number):
        # if not (Professor.get_professor_by_netid(professor_id)):
        #    return None
        post = Post(
            title=title,
            description=description,
            tags=",".join(tags),
            professor_id=professor_id,
            qualifications=qualifications,
            current_students="",
            desired_skills="",
            capacity=1,
            current_number=0
        )
        db.session.add(post)
        db.session.commit()
        return post

    # Keep arguments in alphabetical order!
    @classmethod
    def update_post(cls, post_id,
                    capacity=None, current_number=None, current_students=None,
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
        if current_students:
            post.current_students = current_students
        if desired_skills:
            post.desired_skills = desired_skills
        if capacity:
            post.capacity = int(capacity)
        if current_number:
            post.current_number = int(current_number)
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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags.split(','),
            'qualifications': self.qualifications,
            'professor_id': self.professor_id,
            'current_students': self.current_students,
            'desired_skills': self.desired_skills,
            'capacity': self.capacity,
            'current_number': self.current_number,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }
