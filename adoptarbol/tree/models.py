# -*- coding: utf-8 -*-
"""Tree and sponsorship models."""
import os
import datetime as dt
import utm
from random import randint
from flask import current_app as app
from werkzeug import secure_filename
from sqlalchemy import text

from adoptarbol.database import Column, Model, SurrogatePK, db, reference_col, relationship

def convert_lat(context):
    utm_e = context.current_parameters.get('coord_utm_e')
    utm_n = context.current_parameters.get('coord_utm_n')
    utm_zone_n = context.current_parameters.get('coord_utm_zone_n')
    utm_zone_letter = context.current_parameters.get('coord_utm_zone_letter')
    lat, lon = utm.to_latlon(utm_e, utm_n, utm_zone_n, utm_zone_letter)
    return lat

def convert_lon(context):
    utm_e = context.current_parameters.get('coord_utm_e')
    utm_n = context.current_parameters.get('coord_utm_n')
    utm_zone_n = context.current_parameters.get('coord_utm_zone_n')
    utm_zone_letter = context.current_parameters.get('coord_utm_zone_letter')
    lat, lon = utm.to_latlon(utm_e, utm_n, utm_zone_n, utm_zone_letter)
    return lon


class Tree(SurrogatePK, Model):
    """A tree to adopt."""

    __tablename__ = 'trees'
    code = Column(db.String(80), unique=True, nullable=False)
    common_name = Column(db.String(80), nullable=False)
    scientific_name = Column(db.String(80), nullable=False)
    family = Column(db.String(80), nullable=False)

    photo = Column(db.String(256))

    sponsor = relationship('Sponsorship', backref='tree')

    coord_utm_e = Column(db.Float)
    coord_utm_n = Column(db.Float)
    coord_utm_zone_n = Column(db.Integer, default=19)
    coord_utm_zone_letter = Column(db.String, default='L')

    coord_lat = Column(db.Float, default=convert_lat)
    coord_lon = Column(db.Float, default=convert_lon)

    diameter = Column(db.Integer, nullable=False)
    height = Column(db.Integer, nullable=False)

    comments  = Column(db.String(500))

    cost = Column(db.Float, nullable=False, default=50)
    currency = Column(db.String, nullable=False, default='USD')

    function = Column(db.String(500))

    def __init__(self, code, **kwargs):
        """Create instance."""
        db.Model.__init__(self, code=code, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Tree({id})>'.format(id=self.id)

    @property
    def image(self):
        common_photo_file = "%s.jpg" % secure_filename(self.common_name.lower())
        common_photo_path = os.path.join(app.static_folder, 'images', \
                                        'common_trees', common_photo_file)
        if self.photo:
            return {'exists':True, 'src':self.photo}
        elif os.path.exists(common_photo_path) and os.path.isfile(common_photo_path):
            return {'exists':True, 'src':"/static/images/common_trees/%s" % common_photo_file}
        else:
            return {'exists':False, 'src':"/static/images/common_trees/reference_tree.jpg"}

    @property
    def before(self):
        if self==Tree.query.first():
            return Tree.query.offset(Tree.query.count() - 1).first()

        tree = Tree.get_by_id(self.id - 1)
        return tree or tree.before

    @property
    def after(self):
        if self==Tree.query.offset(Tree.query.count() - 1).first():
            return Tree.query.first()

        tree = Tree.get_by_id(self.id + 1)
        return tree or tree.after

    @classmethod
    def random(cls):
        if cls.query.count() > 0:
            random_id = randint(1, cls.query.count())
            tree = cls.query.offset(random_id).first()
            return tree

    @classmethod
    def adopted(cls):
        return Sponsorship.query.filter(text("status='confirmed'")).count()


class Sponsorship(SurrogatePK, Model):
    """A tree adoption."""

    __tablename__ = 'sponsorships'

    tree_id = reference_col('trees', nullable=True)
    user_id = reference_col('users', nullable=True)

    sponsored_on = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    amount = Column(db.Float, nullable=False)
    currency = Column(db.String, nullable=False)
    reference = Column(db.String, nullable=False)

    status = Column(db.String, nullable=False)
    just_test = Column(db.Boolean(), default=False)

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Sponsorship({code})>'.format(code=self.tree_id)

