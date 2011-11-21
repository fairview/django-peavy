class DjangoDBRouter(object):
    """
    Routes all database operations on peavy models to settings.PEAVY_DATABASE_NAME.
    """

    def db_for_read(self, model, **hints):
        from django.conf import settings
        db_name = getattr(settings, 'PEAVY_DATABASE_NAME', 'peavy')

        db = None
        if model._meta.app_label == 'peavy':
            db = db_name
        return db

    def db_for_write(self, model, **hints):
        from django.conf import settings
        db_name = getattr(settings, 'PEAVY_DATABASE_NAME', 'peavy')

        db = None
        if model._meta.app_label == 'peavy':
            db = db_name
        return db

    def allow_relation(self, obj1, obj2, **hints):
        allow = None

        if obj1._meta.app_label == 'peavy' and obj2._meta.app_label == 'peavy':
            allow = True
        return allow
