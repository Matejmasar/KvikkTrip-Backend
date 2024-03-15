
from geoalchemy2 import Geometry, Geography
from geoalchemy2.elements import WKBElement
from sqlalchemy.orm import relationship
from sqlalchemy import func, Column
from database import db
from src.gps_type import LatLngType
from src.tags_locations import tags_locations


''' Implements the Locations table functionality
 
Attributes:  
    name [string]
    gps  [point]
    id   [integer]
 '''
class Locations(db.Model):
    __tablename__ = 'locations'

    id_location = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    gps = db.Column(Geometry(geometry_type='POINT', srid=4326))
    #gps = db.Column(LatLngType)
    #st_asewkb(CAST (some_point AS geometry))
    #cast(st_as)
    #gps = db.Column(Geometry('POINT'))
    tags = db.relationship('Tags', secondary=tags_locations, back_populates='locations')

    @classmethod
    def get_all_locations(cls):
        #return cls.query().all()
        print(cls.query.all())
        #cls.query(Locations, func.ST_AsEWKB(Locations.gps)).all()
    
    @classmethod
    def get_location_by_id(cls, id_location):
        return cls.query.get(id_location)
    
    @classmethod
    def add_location(cls, name, latitude, longitude):
        new_location = cls(name=name, gps=f'POINT({longitude} {latitude})')
        db.session.add(new_location)
        db.session.commit()
        return new_location   

    @classmethod
    def update_location(cls, location_id, name=None, latitude=None, longitude=None):
        location = cls.query.get(location_id)
        if not location:
            return None  # Location not found

        if name is not None:
            location.name = name
        if latitude is not None and longitude is not None:
            location.gps = f'POINT({longitude} {latitude})'

        db.session.commit()
        return location
    
    @classmethod
    def delete_location(cls, location_id):
        location = cls.query.get(location_id)
        if not location:
            return False  # Location not found

        db.session.delete(location)
        db.session.commit()
        return True
    
    @classmethod
    def serialize(self):
         # Assuming `gps` is a Geometry column.
        # Convert `gps` to WKT (Well-Known Text) for serialization.
        # This requires executing a query to transform the geometry to text.
        #gps_gpt = db.session.query(func.ST_AsText(self.gps)).scalar()
        seralized_point = WKBElement(self.gps.data, srid=self.gps.srid).desc
        return {
            'id_location': self.id_location,
            'name': self.name,
            'gps': seralized_point
        }