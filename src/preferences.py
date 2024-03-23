from database import db

""" Implements the preferences table"""
class Preferences(db.Model):
    __tablename__ = 'preferences'

    id_tag = db.Column(db.Integer, db.ForeignKey('tags.id_tag'), primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key=True)
    weight = db.Column(db.Float)

    user = db.relationship('Users', backref=db.backref('preferences', lazy='dynamic'))
    tag = db.relationship('Tags', backref=db.backref('preferences', lazy='dynamic'))

    @classmethod
    def get_all_preferences(cls):
        return cls.query.all()
    
    @classmethod
    def add_weight(cls, date):
        new_weight = cls(date=date)
        db.session.add(new_weight)
        db.session.commit()
        return new_weight

    @classmethod
    def update_weight(cls, weight_id, new_date):
        weight = cls.query.get(weight_id)
        if not weight:
            return None  # weight not found

        weight.date = new_date
        db.session.commit()
        return weight

    @classmethod
    def delete_weight(cls, weight_id):
        weight = cls.query.get(weight_id)
        if not weight:
            return False  # weight not found

        db.session.delete(weight)
        db.session.commit()
        return True
    
    def serialize(self):
        return {
            'id_weight': self.id_weight,
            'date': self.date
        }

    def __repr__(self):
        return f"<weight id={self.id}, date={self.date}>"


