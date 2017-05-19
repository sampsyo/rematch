from server import db
from werkzeug import generate_password_hash, check_password_hash


class Professor(db.Model):
    __tablename__ = 'professors'
    net_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    password = db.Column(db.String(128))
    website = db.Column(db.String(10000))
    office = db.Column(db.String(10000))
    is_student = False

    # This is for Login Stuff
    is_authenticated = True
    is_active = True
    is_anonymous = True

    def get_id(self):
        return self.net_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_correct_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create_professor(cls, net_id=net_id, name=name,
                         email=email, password=password):
        if Professor.get_professor_by_netid(net_id):
            return None

        professor = Professor(
            net_id=net_id,
            name=name,
            email=email,
            password=password  # Just for demonstration!!!
        )
        db.session.add(professor)
        db.session.commit()
        return professor

    @classmethod
    def update_professor(cls, net_id, name=None, email=None, website=None,
                         office=None):
        professor = Professor.get_professor_by_netid(net_id)
        if not professor:
            return None
        if name:
            professor.name = name
        if email:
            professor.email = email
        if website:
            professor.website = website
        if office:
            professor.office = office
        db.session.commit()
        return professor

    @classmethod
    def get_professor_by_netid(cls, net_id):
        professor = Professor.query.filter(Professor.net_id == net_id).first()
        if professor:
            return professor
        else:
            return None

    @classmethod
    def delete_professor(cls, net_id):
        professor = Professor.get_professor_by_netid(net_id)
        if professor:
            db.session.delete(professor)
            db.session.commit()
            return True
        else:
            return False

    def __init__(self, password, **kwargs):
        super(Professor, self).__init__(**kwargs)
        self.set_password(password)

    @property
    def serialize(self):
        return {
            'net_id': self.net_id,
            'name': self.name,
            'email': self.email,
            'website': self.website,
            'office': self.office
        }

    @classmethod
    def annotate_posts(cls, posts):
        """ Post objects do not included the professor name by default.  This
        function takes a list of posts, and adds a professor_name field to each.
        """
        for post in posts:
            post['professor_name'] = Professor.get_professor_by_netid(
                post['professor_id']).name
