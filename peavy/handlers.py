import logging
import traceback

class ExceptionLoggingHandler(logging.Handler):
    """
    A handler that collects exception information, including a stack trace and
    a full Django error page.
    """

    def get_debug_page(self, record, request):
        """
        Given a logging.LogRecord and a Django request that encountered an
        exception, create a Django server error debugging page.
        """

        from django.views.debug import ExceptionReporter

        debug_page = ""
        if record.exc_info:
            exc_info = record.exc_info
            reporter = ExceptionReporter(request, *exc_info)
            debug_page = reporter.get_traceback_html() or ""
        return debug_page

    def get_stack_trace(self, record, request):
        """
        Given a logging.LogRecord and a Django request that encountered an
        exception, collect a stack trace.
        """

        from django.views.debug import ExceptionReporter

        stack_trace = ""
        if record.exc_info:
            exc_info = record.exc_info
            reporter = ExceptionReporter(request, *exc_info)
            stack_trace = "\n".join(
                traceback.format_exception(*record.exc_info)
            )
        return stack_trace

class DjangoDBHandler(ExceptionLoggingHandler):
    """
    A handler that stores log records in a Django model.
    """
    
    def emit(self, record):
        from django.db import transaction

        from peavy.middleware import RequestLoggingMiddleware
        from peavy.models import LogRecord

        self.format(record)

        request = getattr(RequestLoggingMiddleware.context, "request", None)

        stack_trace = self.get_stack_trace(record, request)
        debug_page = self.get_debug_page(record, request)

        from django.conf import settings
        db_name = getattr(settings, "PEAVY_DATABASE_NAME", "peavy")

        with transaction.commit_on_success(using=db_name):
            LogRecord.objects.using(db_name).create(
                logger = record.name,
                level = record.levelname,
                message = record.msg,
                uuid = getattr(record, "uuid", "?"),
                client_ip = getattr(record, "client_ip", "?"),
                username = getattr(record, "username", "?"),
                user_pk = getattr(record, "user_pk", None),
                stack_trace = stack_trace,
                debug_page = debug_page
            )

class AdminEmailHandler(ExceptionLoggingHandler):
    """
    A handler that sends an abridged error notification to settings.ADMINS; the
    email includes the traceback and a link to the dashboard for reviewing the
    request's log records, but no sensitive data like request.POST.
    """

    def emit(self, record):
        from peavy.middleware import RequestLoggingMiddleware
        from django.core import mail
        from django.core.urlresolvers import reverse
        from django.contrib.sites.models import Site

        subject = "%s: %s" % (
            record.levelname,
            record.msg
        )

        try:
            request = getattr(RequestLoggingMiddleware.context, "request", None)
            site = Site.objects.get_current()
            request_link = (
                "View the log entries for this request:\n\n"
                "https://%s%s?request_id=%s\n" % (
                    site.domain,
                    reverse("peavy:dashboard"),
                    record.uuid
                )
            )

        except Exception, e:
            print e
            request = None
            request_link = "Link to request log records unavailable."

        stack_trace = ""
        if record.exc_info:
            stack_trace = self.get_stack_trace(record, request)

        message = "%s\n\n%s" % (request_link, stack_trace)

        mail.mail_admins(
            subject,
            message,
            fail_silently=True
        )
