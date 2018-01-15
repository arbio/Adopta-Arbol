# -*- coding: utf-8 -*-
"""Tree and sponsorship models."""
import base64
import datetime as dt
import os
from random import randint

import utm
from flask import current_app as app
from sqlalchemy import text
from thumbnails import get_thumbnail
from werkzeug import secure_filename

# from adoptarbol.compat import BytesIO
from adoptarbol.database import Column, Model, SurrogatePK, db, reference_col, relationship
from adoptarbol.extensions import api_manager, pages


def convert_lat(context):
    if context:
        utm_e = context.current_parameters.get('coord_utm_e')
        utm_n = context.current_parameters.get('coord_utm_n')
        utm_zone_n = context.current_parameters.get('coord_utm_zone_n')
        utm_zone_letter = context.current_parameters.get('coord_utm_zone_letter')
        if utm_e and utm_n:
            lat, lon = utm.to_latlon(utm_e, utm_n, utm_zone_n, utm_zone_letter)
            return lat


def convert_lon(context):
    if context:
        utm_e = context.current_parameters.get('coord_utm_e')
        utm_n = context.current_parameters.get('coord_utm_n')
        utm_zone_n = context.current_parameters.get('coord_utm_zone_n')
        utm_zone_letter = context.current_parameters.get('coord_utm_zone_letter')
        if utm_e and utm_n:
            lat, lon = utm.to_latlon(utm_e, utm_n, utm_zone_n, utm_zone_letter)
            return lon


class Tree(SurrogatePK, Model):
    """A tree to adopt."""

    __tablename__ = 'trees'
    code = Column(db.String(80))  # , unique=True)
    common_name = Column(db.String(80), nullable=False)
    scientific_name = Column(db.String(80), nullable=False)
    family = Column(db.String(80), nullable=False)

    photo = Column(db.String(256))

    sponsor = relationship('Sponsorship', backref='tree')

    coord_utm_e = Column(db.Float)
    coord_utm_n = Column(db.Float)
    coord_utm_zone_n = Column(db.Integer, default=19)
    coord_utm_zone_letter = Column(db.String, default='L')

    coord_lat = Column(db.Float)  # , default=convert_lat)
    coord_lon = Column(db.Float)  # , default=convert_lon)

    diameter = Column(db.Integer, nullable=False)
    circ = Column(db.Integer, nullable=False)
    height = Column(db.Integer, nullable=False)

    notes = Column(db.String(500))
    observation = Column(db.String(500))

    surveyed_on = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    base_area = Column(db.Float)
    size_class = Column(db.String(80))
    quality = Column(db.Float)

    cost = Column(db.Float, nullable=False, default=50)
    currency = Column(db.String, nullable=False, default='USD')

    phenology = Column(db.String(500))
    relevance = Column(db.String(500))

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Tree({id})>'.format(id=self.id)

    @property
    def image(self):
        common_photo_file = '%s.jpg' % secure_filename(self.common_name.lower())
        common_photo_path = os.path.join(app.static_folder, 'images',
                                         'common_trees', common_photo_file)
        if self.photo:
            return {'exists': True, 'src': self.photo}
        elif os.path.exists(common_photo_path) and os.path.isfile(common_photo_path):
            return {'exists': True, 'src': '/static/images/common_trees/%s' % common_photo_file}
        else:
            return {'exists': False, 'src': '/static/images/common_trees/reference_tree.jpg'}

    @property
    def before(self):
        if self == Tree.query().first():
            return Tree.query().offset(Tree.query().count() - 1).first()

        tree = Tree.get_by_id(self.id - 1)
        return tree or tree.before

    @property
    def after(self):
        if self == Tree.query().offset(Tree.query().count() - 1).first():
            return Tree.query().first()

        tree = Tree.get_by_id(self.id + 1)
        return tree or tree.after

    @classmethod
    def random(cls):
        if cls.query().count() > 0:
            random_id = randint(1, cls.query.count())
            tree = cls.query.offset(random_id).first()
            return tree

    @classmethod
    def adopted(cls):
        return Sponsorship.query.filter(text("status='confirmed'")).count()

    @classmethod
    def query(cls):
        original_query = db.session.query(cls)
        condition = (Tree.diameter)
        return original_query.filter(condition)


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


def postprocessor(result=None, **kw):
    if 'common_name' in result:
        path = 'especies/' + secure_filename(result['common_name']).lower()
        print('Intentando leer: ' + path)
        page = pages.get(path)
        if page:
            result['description'] = page.html
        else:
            page = pages.get('especies/_generic')
            if page:
                result['description'] = page.html
    if 'photo' in result:
        photos = result['photo'].split(',')
        encoded = {}
        for photo in photos:
            filename = os.path.join('../pictures', photo)
            try:
                thumbnail = get_thumbnail(filename, '200x200', crop='center')
            except FileNotFoundError:
                generic = os.path.join('../pictures', '_generic.jpg')
                thumbnail = get_thumbnail(generic, '200x200', crop='center')
            with open(thumbnail.path, 'rb') as image_file:
                img_str = base64.b64encode(image_file.read())
            # buffer = BytesIO()
            # thumbnail.image.save(buffer, format="JPEG")
            # img_str = base64.b64encode(buffer.getvalue())
            encoded[photo] = img_str.decode('UTF-8')

        result['photos'] = encoded


postprocessors = {'GET_SINGLE': [postprocessor]}

api_manager.create_api(Tree, postprocessors=postprocessors, exclude_columns=['coord_lat', 'coord_lon', 'coord_utm_e',
                       'coord_utm_n', 'coord_utm_zone_n', 'coord_utm_zone_letter'])
api_manager.create_api(Sponsorship)
