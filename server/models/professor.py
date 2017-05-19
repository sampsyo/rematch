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
    is_authenticated = True
    is_active = True
    is_anonymous = True

    def __init__(self, password, **kwargs):
        super(Professor, self).__init__(**kwargs)
        self.set_password(password)


    """Summary: Returns the current professor's net id"""
    def get_id(self):
        return self.net_id


    """Summary: Sets the current professor's password
       Parameters:
            password: the password to be set
    """
    def set_password(self, password):
        self.password = generate_password_hash(password)


    """Summary: Returns whether or not password is the professor's
                password
       Parameters:
            password: the password to be checked against the 
                      professor's password
    """
    def is_correct_password(self, password):
        return check_password_hash(self.password, password)


    """Summary: Creates the current professor object using his or 
                her net id, name, email, and password. Returns the
                professor object if successfully created
       Parameters:
            net id: the professor's net id
            name: the professor's name
            email: the professor's email
            password: the professor's password
    """
    @classmethod
    def create_professor(cls, net_id=net_id, name=name,
                         email=email, password=password):
        if Professor.get_professor_by_netid(net_id):
            return None

        professor = Professor(
            net_id=net_id,
            name=name,
            email=email,
            password=password
        )
        db.session.add(professor)
        db.session.commit()
        return professor


    """Summary: Updates the professor object. Only those fields that 
                have been changed update, the rest remain unchanged
        Parameters: See create_professor
    """
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


    """Summary: Returns the professor object identified by the net_id.
                If no professor object has this id, return None.
       Parameters:
            net_id: the net id of the professor to return
    """
    @classmethod
    def get_professor_by_netid(cls, net_id):
        professor = Professor.query.filter(Professor.net_id == net_id).first()
        if professor:
            return professor
        else:
            return None


    """Summary: Deletes the professor object identified by net_id from the 
                database and return True. If no professor object has this id, 
                delete nothing and return False
       Parameters: 
            net_id: the net id of the professor object to delete
    """
    @classmethod
    def delete_professor(cls, net_id):
        professor = Professor.get_professor_by_netid(net_id)
        if professor:
            db.session.delete(professor)
            db.session.commit()
            return True
        else:
            return False

    """Summary: returns a professor object as a dictionary that can be turned 
    into a json"""
    @property
    def serialize(self):
        return {
            'net_id': self.net_id,
            'name': self.name,
            'email': self.email,
            'website': self.website,
            'office': self.office
        }

    """Summary: Correctly annotates posts.

        Post objects do not included the professor name by default. This
        function takes a list of posts, and adds a professor_name field to each
    """
    @classmethod
    def annotate_posts(cls, posts):
        for post in posts:
            post['professor_name'] = Professor.get_professor_by_netid(
                post['professor_id']).name
