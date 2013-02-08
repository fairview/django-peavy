"""
django-peavy makes it easy to collect and monitor Django application logging.
"""
VERSION = (0, 8, 6)


def get_version():
    return '.'.join((str(d) for d in VERSION))
