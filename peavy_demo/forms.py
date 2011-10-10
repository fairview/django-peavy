from django import forms
from django.utils.translation import gettext_lazy as _

from peavy_demo.models import Quote

class QuoteForm(forms.ModelForm):
    submitter = forms.CharField(label=_("Your name"))
    show = forms.CharField(label=_("The show"))
    character = forms.CharField(label=_("The character"))
    text = forms.CharField(widget=forms.Textarea, label=_("The quote"))

    class Meta:
        model = Quote
        exclude = ['timestamp']
