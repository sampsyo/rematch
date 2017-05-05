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
    date_created = db.Column(db.DateTime,
                            default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                            default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    stale_date = db.Column(db.DateTime)
    contact_email = db.Column(db.String(10000))
    project_link = db.Column(db.String(10000))

    # unimplemented
    required_courses = db.Column(db.String(10000))
    grad_only = db.Column(db.Boolean, default=False)
    qualifications = db.Column(db.String(10000))
    current_students = db.Column(db.String(10000))
    desired_skills = db.Column(db.String(10000))
    capacity = db.Column(db.Integer)
    current_number = db.Column(db.Integer)

    def is_stale(self):
        return self.stale_date is not None and \
            self.stale_date < datetime.datetime.now()

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
                    qualifications, desired_skills, stale_days,
                    contact_email, project_link, required_courses,
                    grad_only):
        # if not (Professor.get_professor_by_netid(professor_id)):
        #    return None
        stale_date = None
        if stale_days:
            stale_date = datetime.datetime.now() + datetime.timedelta(
                days=stale_days
            )

        post = Post(
            title=title,
            description=description,
            tags=",".join(tags),
            professor_id=professor_id,
            qualifications=qualifications,
            desired_skills="",
            stale_date=stale_date,
            contact_email=contact_email,
            project_link=project_link,
            required_courses=required_courses,
            grad_only=grad_only
        )
        #update_tags_from_desc(post)
        db.session.add(post)
        db.session.commit()
        return post

    # Keep arguments in alphabetical order!
    @classmethod
    def update_post(cls, post_id,
                    description=None, desired_skills=None, is_active=None,
                    professor_id=None, qualifications=None, required_courses=None,
                    tags=None, title=None, project_link=None, contact_email=None,
                    grad_only=None):
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
        if project_link is not None:
            post.project_link = project_link
        if contact_email is not None:
            post.contact_email = contact_email
        if required_courses is not None:
            post.required_courses = required_courses
        if grad_only is not None:
            post.grad_only = grad_only
        #if description is not None:
        #    update_tags_from_desc(post)
        db.session.commit()
        return post

    @classmethod
    def update_tags_from_desc(cls, post):
        new_tags = []
        for tag in TAGS:
            if tag in post.description.lower() and tag not in post.tags:
                new_tags.append(tag)
        post.tags = post.tags + "," + ",".join(new_tags)

    @classmethod
    def get_post_by_id(cls, post_id):
        if not post_id:
            return None

        post = Post.query.filter(Post.id == int(post_id)).first()
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

    # considering combining these following two functions
    # def search_posts(cls, courses=None, keywords=None):
    # it will filter out not searched for courses then search that
    # filtered list for the keywords.
    # For now, I just have separate functions

    # first filter by courses if checked
    # then filter by tag section
    # then filter by descrit
    @classmethod
    def get_posts_by_keywords(cls, keywords):
        posts = []
        post_ids = set()
        for p in Post.query.filter_by(is_active=True).all():
            for keyword in keywords.lower():
                if (keyword in p.title.lower()) \
                    or (keyword in p.description.lower()) \
                    or (keyword in p.tags.lower()) \
                    or (keyword in p.professor_id.lower()) \
                    or (keyword in p.desired_skills.lower()) \
                    or (keyword in p.required_courses.lower()):
                    if p.id not in post_ids:
                        post_ids.add(p.id)
                        posts.append(p.serialize_compressed_post)
        return posts

    # returns only the posts that all required courses part of
    # the searched for course list
    @classmethod
    def get_posts_by_courses(cls, courses):
        posts = []
        post_ids = set()
        for p in Post.query.filter_by(is_active=True).all():
            if set(p.required_courses.lower()).issubset(set(courses.lower())):
                if p.id not in post_ids:
                    post_ids.add(p.id)
                    posts.append(p.serialize_compressed_post)
        return posts

    @classmethod
    def search(cls, is_grad=None, taken_courses=None, tags=None, keywords=None):
        search_list = Post.query.filter_by(is_active=True).all()
        print(is_grad)
        print(taken_courses)
        print(tags)
        print(keywords)
        for p in search_list:
            if p.required_courses is None:
                p.required_courses = " "
        if is_grad is not None:
            for p in list(search_list):
                if p.grad_only and not is_grad:
                    search_list.remove(p)
        if taken_courses is not None:
            for p in list(search_list):
                if not set(p.required_courses.lower()).issubset(set(taken_courses.lower())):
                    search_list.remove(p)
        if tags is not None:
            for p in list(search_list):
                if len(set(tags.lower()).intersection(set(p.tags.lower()))) == 0: #no overlap in searched tags vs post tags
                    search_list.remove(p)
        if keywords is not None:
            for p in list(search_list):
                if len(set(keywords.lower()).intersection(set(p.title.lower()))) == 0 \
                    and len(set(keywords.lower()).intersection(set(p.description.lower()))) == 0 \
                    and len(set(keywords.lower()).intersection(set(p.professor_id.lower()))) == 0 \
                    and len(set(keywords.lower()).intersection(set(p.desired_skills.lower()))) == 0:
                        search_list.remove(p)
        posts = []
        for p in search_list:
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
            'stale_date': self.stale_date,
            'project_link': self.project_link,
            'contact_email': self.contact_email,
            'required_courses': self.required_courses,
            'grad_only': self.grad_only
        }

    @property
    def serialize_compressed_post(self):
        return {
            'id': self.id,
            'title': self.title,
            # only 60 words
            'description': (
                " ".join(self.description.split(" ")[:60]) + '...'
                if len(self.description.split(" ")) > 60 else self.description),
            # only 5 tags
            'tags': self.tags.split(',')[:5],
            'professor_id': self.professor_id,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    @classmethod
    def empty(cls):
        return {
            'id': '',
            'title': '',
            'description': '',
            'tags': '',
            'qualifications': '',
            'professor_id': '',
            'desired_skills': '',
            'is_active': '',
            'date_created': '',
            'date_modified': '',
            'stale_date': '',
            'project_link': '',
            'contact_email': '',
            'required_courses': '',
            'grad_only': ''
        }

    TAGS = [
        'artificial intelligence',
        'computer architecture',
        'computational biology',
        'databases',
        'education',
        'graphics',
        'human computer interaction',
        'operating systems',
        'networking',
        'programming languages',
        'scientific computing',
        'security',
        'theory',
        'natural language processing',
        'algorithms',
        'distributed systems',
        'robotics',
        'information processing',
        'computer vision',
        'ethics',
        'design',
        'compilers',
        'machine learning',
        'other',
        'java',
        'c',
        'c#',
        'c++',
        'python',
        'ocaml',
        'javascript',
        'mongodb',
        'sql'
    ]
