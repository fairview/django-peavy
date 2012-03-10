import datetime
import socket

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class LogRecord(models.Model):
    """
    A simple bucket for the usual logging info (logger, level, message) plus a
    unique request ID for tracking all the log records made in a given request,
    the server logging the request, the client's IP address, the name of the
    application, and for requests with errors, a stack trace and a copy of
    Django's server error page.
    """
    timestamp = models.DateTimeField(db_index=True, default=datetime.datetime.now)

    application = models.CharField(
        max_length=256,
        default=getattr(
            settings,
            'PEAVY_APP_NAME',
            settings.ROOT_URLCONF.split('.')[0]
        ),
        help_text=_("The application logging this record."),
        db_index=True
    )

    origin_server = models.CharField(
        max_length=256,
        help_text=_("The server logging this record."),
        default=socket.gethostname,
        db_index=True
    )

    client_ip = models.CharField(
        max_length=128,
        help_text=_("The IP address of the client making the request."),
        blank=True,
        db_index=True
    )

    user_pk = models.IntegerField(
        blank=True,
        null=True,
        db_index=True,
        help_text=_("The primary key of the user making the request in which this record was logged."),
    )

    username = models.CharField(
        max_length=256,
        help_text=_("The username of the user making the request in which this record was logged."),
        blank=True,
        db_index=True
    )

    uuid = models.CharField(
        max_length=256,
        help_text=_("The UUID of the Django request in which this record was logged."),
        blank=True,
        db_index=True
    )

    logger = models.CharField(
        max_length=1024,
        help_text=_("The name of the logger of the record."),
        db_index=True
    )

    level = models.CharField(
        max_length=32,
        help_text=_("The level of the log record (DEBUG, INFO...)"),
        db_index=True
    )

    message = models.TextField()
    stack_trace = models.TextField(blank=True)
    debug_page = models.TextField(blank=True)

    class Meta:
        ordering = ('-timestamp',)
        permissions = (
            ("view_logs", "Can view log records"),
        )

    def __unicode__(self):
        return unicode(self.pk)
