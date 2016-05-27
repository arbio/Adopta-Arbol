# -*- coding: utf-8 -*-
"""Tree and sponsorship models."""
import datetime as dt

from adoptarbol.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Tree(SurrogatePK, Model):
    """A tree to adopt."""

    __tablename__ = 'trees'
    code = Column(db.String(80), unique=True, nullable=False)
    common_name = Column(db.String(80), nullable=False)
    scientific_name = Column(db.String(80), nullable=False)
    family = Column(db.String(80), nullable=False)

    sponsor = relationship('Sponsorship', backref='tree')

    coord_utm_e = Column(db.Float, nullable=False)
    coord_utm_n = Column(db.Float, nullable=False)

    diameter = Column(db.Integer, nullable=False)
    height = Column(db.Integer, nullable=False)

    comments  = Column(db.String(500), nullable=True)

    def __init__(self, code, **kwargs):
        """Create instance."""
        db.Model.__init__(self, code=code, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Tree({code})>'.format(code=self.code)


class Sponsorship(SurrogatePK, Model):
    """A tree adoption."""

    __tablename__ = 'sponsorships'
    code = Column(db.String(80), unique=True, nullable=False)

    tree_id = reference_col('trees', nullable=True)
    user_id = reference_col('users', nullable=True)

    amount = Column(db.Float, nullable=False)
    currency = Column(db.String, nullable=False)
    reference = Column(db.String, nullable=False)

    def __init__(self, code, **kwargs):
        """Create instance."""
        db.Model.__init__(self, code=code, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Sponsorship({code})>'.format(code=self.tree_id)

