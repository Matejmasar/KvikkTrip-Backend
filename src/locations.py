
from database import db
from src.tags_locations import tags_locations


''' Implements the Locations table functionality
 
Attributes:  
    name [string]
    gps  [string]
    id   [integer]
 '''
class Locations(db.Model):
    __tablename__ = 'locations'

    id_location = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    gps = db.Column(db.String)
    tags = db.relationship('Tags', secondary=tags_locations, back_populates='locations')

    @classmethod
    def get_all_locations(cls):
        return cls.query.all()
    
    @classmethod
    def get_location_by_id(cls, id_location):
        return db.session.get(cls, id_location)
    
    @classmethod
    def add_location(cls, name, latitude, longitude):
        gps = f'({latitude}, {longitude})'
        new_location = cls(name=name, gps=gps)
        try:
            db.session.add(new_location)
            db.session.commit()
            return new_location.serialize()
        except Exception as e:
            db.session.rollback()
            print (e.args[0])
            return None

    @classmethod
    def update_location(cls, location_id, name=None, latitude=None, longitude=None):
        location = db.session.get(cls, location_id)
        if not location:
            return None  # Location not found

        if name is not None:
            location.name = name
        if latitude is not None and longitude is not None:
            location.gps = f'({latitude}, {longitude})'

        db.session.commit()
        return location
    
    @classmethod
    def delete_location(cls, location_id):
        location = db.session.get(cls, location_id)
        if not location:
            return False  # Location not found

        db.session.delete(location)
        db.session.commit()
        return True
    
    def serialize(self):
        return {
            'id_location': self.id_location,
            'name': self.name,
            'gps': self.gps
        }