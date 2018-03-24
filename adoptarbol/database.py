# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship

from .compat import basestring
from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship


# Create customized model view class
class RestrictedModelView(ModelView):
    page_size = 12
    column_exclude_list = ['photo', 'coord_utm_e', 'coord_utm_n', 'coord_utm_zone_letter',
                           'coord_utm_zone_n', 'coord_lat', 'coord_lon', 'circ', 'height',
                           'cost', 'currency', 'family', 'password']

    # create_modal = True
    # edit_modal = True
    def process_ref(view, context, model, name):
        return model.__reference__
    column_formatters = dict(reference=process_ref)

    def is_accessible(self):
        return current_user.is_authenticated


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True

    def __getitem__(self, key):
        """Expose object attributes like dict values."""
        return getattr(self, key)

    def keys(self):
        """Identify what db columns we have."""
        return inspect(self).attrs.keys()


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
