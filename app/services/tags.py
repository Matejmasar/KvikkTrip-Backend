from database import db
from sqlalchemy.orm import relationship
from app.services.tags_locations import tags_locations


"""Implements the Tags table """
class Tags(db.Model):
    __tablename__ = 'tags'

    id_tag = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256))
    locations = relationship('Locations', secondary=tags_locations, back_populates='tags')

    @classmethod
    def get_all_tags(cls):
        return cls.query.all()
    
    @classmethod
    def get_tab_by_id(cls, id_tags):
        return db.session.get(cls, id_tags)
    
    @classmethod
    def add_tag(cls, label):
        new_tag = cls(label=label)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    @classmethod
    def update_tag(cls, tag_id, new_label):
        tag = cls.query.get(tag_id)
        if not tag:
            return None  # Tag not found

        tag.label = new_label
        db.session.commit()
        return tag

    @classmethod
    def delete_tag(cls, tag_id):
        tag = cls.query.get(tag_id)
        if not tag:
            return False  # Tag not found

        db.session.delete(tag)
        db.session.commit()
        return True
    
    @classmethod
    def does_exist(cls, label):
        tag = cls.query.filter_by(label=label).first()
    
    def serialize(self):
        return {
            'id_tag': self.id_tag,
            'label': self.label
        }

    def __repr__(self):
        return f"<Tag id={self.id}, label={self.label}>"


