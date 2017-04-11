from server import db


class Professor(db.Model):
    __tablename__ = 'professors'
    net_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    desc = db.Column(db.String(10000))
    interests = db.Column(db.String(10000))

    @classmethod
    def create_professor(cls, net_id=net_id, name=name):
        if Professor.get_professor_by_netid(net_id):
            print("Professor already exists with net_id %s" % net_id)
            return None

        professor = Professor(
            net_id=net_id,
            name=name,
            email=net_id + "@cornell.edu"
        )
        db.session.add(professor)
        db.session.commit()
        return professor

    @classmethod
    def update_professor(cls, net_id, name=None, email=None, desc=None, interests=None): 
        professor = Professor.get_professor_by_netid(net_id) 
        if not professor: 
            return None 
        if name: 
            professor.name = name 
        if email: 
            professor.email = email 
        if desc: 
            professor.desc = desc 
        if interests: 
            professor.interests = interests
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
    def get_all_professors(cls):
        return [s.serialize for s in Professor.query.all()]

    @classmethod
    def delete_professor(cls, net_id):
        professor = Professor.get_professor_by_netid(net_id)
        if professor:
            db.session.delete(professor)
            db.session.commit()
            return True
        else:
            return False

    # This is to convert calls for User into json friendly format!
    @property
    def serialize(self):
        return {
            'net_id': self.net_id,
            'name': self.name,
            'email': self.email,
            # 'posts': self.posts,
            'desc': self.desc,
            'interests': self.interests
        }
