from db import db


class IssueModel(db.Model):
    __tablename__ = 'issue'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(500))
    status = db.Column(db.String(20))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, assigned_to, created_by, status):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.created_by = created_by
        self.status = status

    def json(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'assigned_to': self.assigned_to, 'created_by': self.created_by, 'status': self.status}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, issue_id):
        return cls.query.filter_by(id=issue_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
