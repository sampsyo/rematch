import datetime
from server import db
from config import PAGINATION_PER_PAGE
from sqlalchemy import desc, or_, and_
# from server.models.professor import Professor


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(10000))
    professor_id = db.Column(db.String(64), db.ForeignKey('professors.net_id'))
    tags = db.Column(db.String(10000))
    required_courses = db.Column(db.String(10000))
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
    qualifications = db.Column(db.String(10000))
    desired_skills = db.Column(db.String(10000))

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
                  active_only=False, inactive_only=False,
                  professor_id=None, keywords=None, tags=None,
                  required_courses=None):
        """
            page: current page of pagination, else None to get all posts
            compressed: True to get the compressed serialization
            descend: True to order descending by post id (creation)
            active_only: Only show active posts
            inactive_only: Only show inactive posts
            grad_only: True to only show listings for graduate listings
            professor_id: string, usually netid
            keywords: a string of keywords, exact match searched in the
                title and description of a post
            tags: a string of tags, separated by a comma; posts must have at
                least one tag
        """

        # Build a query object
        query = Post.query
        if active_only:
            query = query.filter_by(is_active=True)
        if inactive_only:
            query = query.filter_by(is_active=False)
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
        if required_courses:
            required_courses = required_courses.strip().lower().split(',')
            query = query.filter(and_(Post.required_courses.contains(c) for c in
                                      required_courses))

        if descend:
            query = query.order_by(desc(Post.id))

        number_pages = 1 
        if page is None:
            posts = query.all()
            has_next = None
        else:
            pagination = query.paginate(page=page, per_page=PAGINATION_PER_PAGE)
            has_next = pagination.has_next
            posts = pagination.items
            number_pages = pagination.pages

        if compressed:
            return ([p.serialize_compressed_post for p in posts], has_next, number_pages)
        else:
            return ([p.serialize for p in posts], has_next, number_pages)

    @classmethod
    def create_post(cls, title, description, professor_id, tags,
                    qualifications, desired_skills, stale_days,
                    contact_email, project_link, required_courses):
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
            desired_skills=desired_skills,
            stale_date=stale_date,
            contact_email=contact_email,
            project_link=project_link,
            required_courses=required_courses,
        )
        # update_tags_from_desc(post)
        db.session.add(post)
        db.session.commit()
        return post

    # Keep arguments in alphabetical order!
    @classmethod
    def update_post(cls, post_id,
                    description=None, desired_skills=None, is_active=None,
                    professor_id=None, qualifications=None, tags=None,
                    required_courses=None, title=None, project_link=None,
                    contact_email=None):
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

        db.session.commit()
        return post

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
    def get_posts_by_courses(cls, courses):
        posts = []
        post_ids = set()
        for p in Post.query.filter_by(is_active=True).all():
            if set(p.required_courses.lower()).issubset(set(courses.lower())):
                if p.id not in post_ids:
                    post_ids.add(p.id)
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
            'courses': self.required_courses.split(','),
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

    COURSES = [
        'CS 2110',
        'CS 3110',
        'CS 4410',
        'CS 4411',
        'CS 4670',
        'CS 4700',
        'CS 4710',
        'CS 4780',
        'CS 5150',
        'CS 5152',
        'CS 5414',
        'INFO 3450',
        'INFO 4300'
    ]
