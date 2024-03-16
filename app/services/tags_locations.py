from database import db

''' Implements the Tags and Locations Class relationship

Attributes:  
    id_tags         [integer]
    id_location    [integer]
 '''
tags_locations = db.Table('tags_locations',
    db.Column('id_tag', db.Integer, db.ForeignKey('tags.id_tag'), primary_key=True),
    db.Column('id_location', db.Integer, db.ForeignKey('locations.id_location'), primary_key=True)
)