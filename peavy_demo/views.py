import logging

from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from peavy_demo.forms import QuoteForm
from peavy_demo.models import Quote

@transaction.commit_on_success
def home(request):
    logger = logging.getLogger('peavy_demo.views.home')

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save()
            logger.info('Quote from {0} in {1} submitted by {2}'.format(quote.character, quote.show, quote.submitter))

            return HttpResponseRedirect(reverse('home'))
    else:
        form = QuoteForm()

    data = {
        'form': form,
        'quotes': Quote.objects.all()
    }

    return render_to_response('home.html', data, context_instance=RequestContext(request))
