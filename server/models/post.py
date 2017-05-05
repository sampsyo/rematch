import datetime
from server import db
from config import PAGINATION_PER_PAGE
from sqlalchemy import desc, or_
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
    def get_posts(cls, page=None, compressed=False, descend=True,
                  active_only=True, inactive_only=False, grad_only=False,
                  professor_id=None, keywords=None, tags=None):
        """
            page: current page of pagination, else None to get all posts
            compressed: True to get the compressed serialization
            descend: True to order descending by post id (creation)
            active_only: Only show active posts
            inactive_only: Only show inactive posts
            grad_only: True to only show listings for graduate listings
            professor_id: string, usually netid
            id: int of post id to find
            keywords: a string of keywords, exact match searched in the
                title and description of a post
            tags: a string of tags, separated by a comma; posts must have at
                least one tag
        """

        # Build a query object
        query = Post.query
        if active_only:
            query = query.filter_by(is_active=True)
        if grad_only:
            query = query.filter_by(grad_only=True)
        if professor_id:
            query = query.filter_by(professor_id=professor_id)

        # search features
        if keywords:
            keywords = keywords.lower().strip()
            query = query.filter(or_(
                Post.description.contains(keywords),
                Post.title.contains(keywords)
            ))
        if tags:
            tags = tags.strip().lower().split(',')
            query = query.filter(or_(Post.tags.contains(tag) for tag in tags))

        if descend:
            query = query.order_by(desc(Post.id))

        if page is None:
            posts = query.all()
            has_next = None
        else:
            pagination = query.paginate(page=page, per_page=PAGINATION_PER_PAGE)
            has_next = pagination.has_next
            posts = pagination.items

        if compressed:
            return ([p.serialize_compressed_post for p in posts], has_next)
        else:
            return ([p.serialize for p in posts], has_next)

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
        # update_tags_from_desc(post)
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
