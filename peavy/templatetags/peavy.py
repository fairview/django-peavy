import re

from django.conf import settings
from django import http
from django import template
from django.utils.html import fix_ampersands
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = template.Library()

PAGE_RE = re.compile("[\?&]page=\d+")
class PageNavigatorNode(template.Node):
    """
    Renders page navigation markup for a page of a django.core.paginator.Paginator.
    """
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url
    
    def render(self, context):
        page = template.Variable(self.page).resolve(context)
        url = template.Variable(self.base_url).resolve(context)
        url = PAGE_RE.sub("", url)
        url = url.replace("%", "%%")
        
        pages = page.paginator.num_pages

        page_link = u'<a class="pagelink %%s" href="%s%spage=%%s"><img src="%s%%s" alt=""></a>' % (url, url.find("?") == -1 and  "?" or "&", settings.STATIC_URL)
        first = getattr(settings, "PAGE_ICON_FIRST", "peavy/img/first.png")
        prev = getattr(settings, "PAGE_ICON_PREV", "peavy/img/prev.png")
        next = getattr(settings, "PAGE_ICON_NEXT", "peavy/img/next.png")
        last = getattr(settings, "PAGE_ICON_LAST", "peavy/img/last.png")

        output = ""
        if page.paginator.num_pages > 1:
            output = u'<div class="page_navigator">%s: ' % _(u"Page")
            output += page_link % ("first", 1, first)
            if page.has_previous:
                output += page_link % ("previous", page.previous_page_number(), prev)
            output += " %s / %s " % (page.number, pages)
            if page.has_next:
                output += page_link % ("next", page.next_page_number(), next)
            output += page_link % ("last", pages, last)                
            output += "</div>"
        return mark_safe(fix_ampersands(output))

@register.tag
def pagenavigator(parser, argument_string):
    argv = argument_string.split_contents()
    argc = len(argv)
    if argc == 3:
        return PageNavigatorNode(argv[1], argv[2])
    
    raise template.TemplateSyntaxError("The %s tag requires a paginator page and a base URL." % argv[0])

class QueryStringNode(template.Node):
    """
    Updates the current query string of the request with the supplied
    parameters and values.

    Values are first looked up as variables in the request context; if the
    variable is not found they'll be used as given.

    You can add or delete specific values, or by passing an empty value, remove
    all values for a parameter. The order in which you pass the parameters is
    the order in which the operations will be applied to the query string.

    Add several parameters:

        {% query_string "level=ERROR" "level=WARN" "logger=record.logger" %}

    Delete a value, if present:

        {% query_string "level-=record.level" %}

    Clear all values for a certain parameter, then add one for it:

        {% query_string "level=" "level=CRITICAL" %}

    """
    parameters = []

    def __init__(self, parameters):
        self.parameters = parameters
    
    def render(self, context):

        operations = []

        for p in self.parameters:
            if '-=' in p:
                # handle requests to delete a specific value
                k, v = p.split('-=', 1)
                operations.append(('delete', k, v))
            else:
                k, v = p.split('=', 1)
                if not v:
                    # handle requests to remove all values
                    operations.append(('clear', k, v))
                else:
                    # add a value for the key
                    operations.append(('add', k, v))
        request = template.Variable('request').resolve(context)

        qs = request.GET.copy()
        for operation, k, v in operations: 
            try:
                k = template.Variable(k).resolve(context)
            except template.VariableDoesNotExist, e:
                # OK, we'll use the key as given
                pass

            if operation == 'clear':
                if k in qs:
                    del qs[k]
                continue

            try:
                v = template.Variable(v).resolve(context)
            except template.VariableDoesNotExist, e:
                # OK, we'll use the value as given
                pass

            if operation == 'add':
                values = qs.getlist(k)
                if v not in values:
                    # repeating parameters is OK, but there's no point repeating
                    # the same values
                    values.append(v)
                    qs.setlist(k, values)

            elif operation == 'delete':
                if k in qs:
                    values = qs.getlist(k)
                    qs.setlist(k, [val for val in values if val != v])

        query_string = qs.urlencode()
        if query_string:
            return '?' + query_string
        else:
            return ''

@register.tag
def query_string(parser, argument_string):
    argv = argument_string.split_contents()
    argc = len(argv)

    return QueryStringNode(argv[1:])
