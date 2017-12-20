from server import db, app
from sqlalchemy import desc, or_, not_
from server.utils import send_email


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(10000))
    professor_id = db.Column(db.String(64), db.ForeignKey('professors.net_id'))
    tags = db.Column(db.String(10000))
    required_courses = db.Column(db.String(10000))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    stale_date = db.Column(db.DateTime)
    contact_email = db.Column(db.String(10000))
    project_link = db.Column(db.String(10000))
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(db.DateTime, default=db.func.now(),
                              onupdate=db.func.now())


    """Summary: Searches and returns posts by keywords, tags, and required courses.
       Parameters:
            page:current page of pagination, else None to get all posts.
            compressed: True to get the compressed serialization
            descend: True to order descending by post id (creation)
            active_only: Only show active posts
            inactive_only: Only show inactive posts
            professor_id: string, usually netid
            keywords: a string of keywords, exact match searched in the
                title and description of a post
            tags: a string of tags, separated by a comma; posts must have at
                least one tag
            stale: True to only show stale listings
    """
    @classmethod
    def get_posts(cls, page=None, compressed=False, descend=True,
                  active_only=False, inactive_only=False,
                  professor_id=None, keywords=None, tags=None,
                  required_courses=None, stale=None):
        # Build a query object
        query = Post.query
        if active_only:
            query = query.filter_by(is_active=True)
        if inactive_only:
            query = query.filter_by(is_active=False)
        if professor_id:
            query = query.filter_by(professor_id=professor_id)
        if stale:
            query = query.filter(Post.stale_date < db.func.now())

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
            unsat_courses = set(
                [x.lower() for x in app.config['COURSES']]
            ).difference(set(required_courses))

            query = query.filter(not_(
                or_(Post.required_courses.contains(x) for x in unsat_courses)
            ))

        if descend:
            query = query.order_by(desc(Post.id))

        number_pages = 1
        if page is None:
            posts = query.all()
            has_next = None
        else:
            pagination = query.paginate(
                page=page,
                per_page=app.config['PAGINATION_PER_PAGE']
            )
            has_next = pagination.has_next
            posts = pagination.items
            number_pages = pagination.pages

        if compressed:
            return ([p.serialize_compressed_post for p in posts],
                    has_next, number_pages)
        else:
            return ([p.serialize for p in posts], has_next, number_pages)


    """Summary: Returns the post identified by post_id if it exists.
                Otherwise return None.
       Parameters:
            post_id: the unique integer identifier for a post
    """
    @classmethod
    def get_post_by_id(cls, post_id):
        if not post_id:
            return None

        post = Post.query.filter(Post.id == int(post_id)).first()
        if post:
            return post
        else:
            return None


    """Summary: Creates and stores a professor's new projects. Returns
                the project object if successfully created.
       Parameters:
            title: the project title
            description: the project description
            professor_id: the project professor's net id
            tags: the tags associated with the project
            stale_date: the project's expiration date
            contact_email: the professor's preferred contact email
            project_link: the link to the project's website
            required_courses: the courses required to have taken for the
                              project
    """
    @classmethod
    def create_post(cls, title=None, description=None, professor_id=None,
                    tags=None, stale_date=None, contact_email=None,
                    project_link=None, required_courses=None):
        if None in (title, description, professor_id, tags, stale_date,
                    contact_email, project_link, required_courses):
            return None
        post = Post(
            title=title,
            description=description.replace('<br>', '\n'),
            tags=",".join(tags),
            professor_id=professor_id,
            stale_date=stale_date,
            contact_email=contact_email,
            project_link=project_link,
            required_courses=''.join(required_courses),
        )
        db.session.add(post)
        db.session.commit()
        return post


    """Summary: Updates a post based on post_id. Only updates those
                fields that have changed.
       Parameters: See create_post
    """
    @classmethod
    def update_post(cls, post_id,
                    description=None, is_active=None,
                    professor_id=None, tags=None,
                    required_courses=None, title=None, project_link=None,
                    contact_email=None, stale_date=None):
        post = Post.get_post_by_id(post_id)
        if not post:
            return None
        if title:
            post.title = title
        if description:
            post.description = description.replace('<br>', '\n')
        if tags:
            post.tags = ",".join(tags)
        if professor_id:
            post.professor_id = professor_id
        if is_active is not None:
            post.is_active = is_active
        if project_link is not None:
            post.project_link = project_link
        if contact_email is not None:
            post.contact_email = contact_email
        if required_courses is not None:
            post.required_courses = required_courses
        if stale_date:
            post.stale_date = stale_date

        db.session.commit()
        return post


    """Summary: Deletes the post identified from the database
       Parameters:
            post_id: the id of the post to be deleted
    """
    @classmethod
    def delete_post(cls, post_id):
        # This method is currently not in use.
        post = Post.get_post_by_id(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        else:
            return False


    """Summary: returns a post as a dictionary that can be turned into a json"""
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags.split(','),
            'professor_id': self.professor_id,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'stale_date': self.stale_date,
            'project_link': self.project_link,
            'contact_email': self.contact_email,
            'courses': self.required_courses.split(',')if self.required_courses
            else []
        }


    """Summary: returns a subsection of a post's information which convey's the
                post's most important information including id, title,
                description, tags, professor id, whether the post is active,
                the date the post was created, and the post's most recent
                modification date
    """
    @property
    def serialize_compressed_post(self):
        return {
            'id': self.id,
            'title': self.title,
            # only 60 words
            'description': " ".join(self.description.split(" ")[:60]) + '...',
            # only 5 tags
            'tags': self.tags.split(',')[:5],
            'professor_id': self.professor_id,
            'is_active': self.is_active,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }


    """Summary: A dictionary representation of an empty post object"""
    @classmethod
    def empty(cls):
        return {
            'id': '',
            'title': '',
            'description': '',
            'tags': '',
            'professor_id': '',
            'is_active': '',
            'date_created': '',
            'date_modified': '',
            'stale_date': '',
            'project_link': '',
            'contact_email': '',
            'required_courses': '',
        }


    """Summary: Automatic disabling of stale posts.

            Triggered by a scheduler that is initialized in server/__init__.py
            Triggeredrigger interval is once per day.
    """
    @staticmethod
    def disable_stale_posts():
        print 'Running stale post scheduler.'
        stale_posts, _, _ = Post.get_posts(active_only=True, stale=True)
        print stale_posts
        for post in stale_posts:
            print 'Setting post %s to inactive.' % post['id']
            Post.update_post(post['id'], is_active=False)
            send_email(post['contact_email'],
                       'Your research listing has expired',
                       'Just to let you know!')
