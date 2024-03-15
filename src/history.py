from database import db

""" Implements the History table"""
class History(db.Model):
    __tablename__ = 'history'

    date= db.Column(db.Date, primary_key=True)
    id_location = db.Column(db.Integer, db.ForeignKey('locations.id_location'), primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), primary_key=True)
    
    user = db.relationship('Users', backref=db.backref('history', lazy='dynamic'))
    location = db.relationship('Locations', backref=db.backref('history', lazy='dynamic'))


    @classmethod
    def get_all_events(cls):
        return cls.query.all()
    
    @classmethod
    def add_event(cls, date):
        new_event = cls(date=date)
        db.session.add(new_event)
        db.session.commit()
        return new_event

    @classmethod
    def update_event(cls, event_id, new_date):
        event = cls.query.get(event_id)
        if not event:
            return None  # event not found

        event.date = new_date
        db.session.commit()
        return event

    @classmethod
    def delete_event(cls, event_id):
        event = cls.query.get(event_id)
        if not event:
            return False  # event not found

        db.session.delete(event)
        db.session.commit()
        return True
    
    @classmethod
    def serialize(self):
        return {
            'id_event': self.id_event,
            'date': self.date
        }

    def __repr__(self):
        return f"<event id={self.id}, date={self.date}>"




