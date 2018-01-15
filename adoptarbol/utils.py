# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from werkzeug import secure_filename
import os


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def secure_path(path):
    dirname = os.path.dirname(path)
    filename = os.path.basename(path)
    file_base, file_ext = os.path.splitext(path)

    dirname = secure_filename(dirname)
    file_base = secure_filename(file_base)
    file_ext = secure_filename(file_ext)

    if file_ext:
        filename = '.'.join([file_base, file_ext])
    else:
        filename = file_base

    if len(filename) > 200:
        filename = '%s__%s' % (filename[:99], filename[-99:])

    if dirname:
        return os.path.join(dirname, filename)

    return filename
