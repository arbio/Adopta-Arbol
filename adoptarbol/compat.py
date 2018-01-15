# -*- coding: utf-8 -*-
"""Python 2/3 compatibility module."""
import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    from cStringIO import StringIO as BytesIO
    text_type = unicode  # noqa
    binary_type = str
    string_types = (str, unicode)  # noqa
    unicode = unicode  # noqa
    basestring = basestring  # noqa
else:
    from io import BytesIO
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)

try:
    FileNotFoundError = FileNotFoundError
except NameError:
    FileNotFoundError = IOError
BytesIO = BytesIO
