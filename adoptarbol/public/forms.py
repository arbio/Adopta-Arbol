# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired

from adoptarbol.user.models import User

import time
import hashlib
import random

class SponsorshipForm(Form):
    """Sponsorship form."""

    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    gift = BooleanField('Es un regalo')

    ## Payments
    opcode = HiddenField('opcode')
    pp_button_id = HiddenField('pp_button_id')
    pp_target = HiddenField('pp_target')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(SponsorshipForm, self).__init__(*args, **kwargs)

        # Generate random hash
        data = '%s%s' % (time.time(), random.randint(10000, 100000))
        random_hash = hashlib.sha1(data.encode('utf-8')).hexdigest()
        self.opcode = random_hash

        if kwargs['sandbox']:
            self.pp_button_id = '5Q34E2APFU3JJ'
            self.pp_target = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
        else:
            self.pp_button_id = 'S9SN2KJFZZBX6'
            self.pp_target = 'https://www.paypal.com/cgi-bin/webscr'

    def validate(self):
        """Validate the form."""
        initial_validation = super(SponsorshipForm, self).validate()
        if not initial_validation:
            return False

        """
        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        """

        return True


class LoginForm(Form):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        return True
