import re

from django.conf import settings
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.core.paginator import EmptyPage, Paginator
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum, Q
from django import http
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from peavy.models import LogRecord

@permission_required("peavy.view_logs")
def dashboard(request):
    """
    The main view: all the logs, with filters and pagination.
    """
    
    records = LogRecord.objects.all()

    applications = request.GET.getlist("application")
    if applications:
        records = records.filter(application__in=applications)

    client_ips = request.GET.getlist("client_ip")
    if client_ips:
        records = records.filter(client_ip__in=client_ips)

    levels = request.GET.getlist("level")
    if levels:
        records = records.filter(level__in=levels)

    loggers = request.GET.getlist("logger")
    if loggers:
        records = records.filter(logger__in=loggers)

    origin_servers = request.GET.getlist("origin_server")
    if origin_servers:
        records = records.filter(origin_server__in=origin_servers)

    request_ids = request.GET.getlist("request_id")
    if request_ids:
        records = records.filter(uuid__in=request_ids)

    show_anonymous_users = False
    user_pks = []
    for pk in request.GET.getlist("user_pk"):
        if pk == "None":
            show_anonymous_users = True
        else:
            user_pks.append(pk)

    user_pk_filter = None

    if show_anonymous_users:
        user_pk_filter = Q(user_pk__isnull=True)

    if user_pks:
        if not user_pk_filter:
            user_pk_filter = Q(user_pk__in=user_pks)
        else:
            user_pk_filter |= Q(user_pk__in=user_pks)
    
    if user_pk_filter:
        records = records.filter(user_pk_filter)

    usernames = request.GET.getlist("username")
    if usernames:
        records = records.filter(username__in=usernames)

    message_filters = request.GET.getlist("message")
    if message_filters:
        message_query = None
        for term in message_filters:
            if not term:
                continue
            if message_query is None:
                message_query = Q(message__iregex=term)
            else:
                message_query &= Q(message__iregex=term)
        if message_query is not None:
            records = records.filter(message_query)

    page_number = int(request.GET.get("page", 1))
    count = int(request.GET.get("count", 20))

    paginator = Paginator(object_list=records, per_page=count, allow_empty_first_page=True)

    if page_number < 1:
        redirect = re.sub("page=\d+", "page=%s" % paginator.num_pages, request.get_full_path())
        return http.HttpResponseRedirect(redirect)
    if page_number > paginator.num_pages:
        redirect = re.sub("page=\d+", "page=1", request.get_full_path())
        return http.HttpResponseRedirect(redirect)

    records = paginator.page(page_number)

    data = {
        "records": records,
    }

    return render_to_response(
        "peavy/dashboard.html",
        data,
        context_instance = RequestContext(request)
    )

@user_passes_test(lambda u: u.is_superuser)
def debug_page(request, record_id):
    """
    For log records with exception information, return the copy of Django's
    error page for the request. As this can contain sensitive information like
    passwords in POST data, restrict the view to superusers.
    """

    record = get_object_or_404(LogRecord, pk=record_id)
    return http.HttpResponse(record.debug_page)
