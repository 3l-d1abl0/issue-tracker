from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(100))
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    access_token = db.Column(db.String(150))

    #issues = db.relationship('IssueModel', lazy='dynamic')

    def __init__(self, email, username, password, first_name, last_name):
        self.email = email
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def json(self):
        return {'id': self.id, 'email': self.email, 'username': self.username, 'password': self.password, 'first_name': self.first_name, 'last_name': self.last_name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
