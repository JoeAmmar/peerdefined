from __future__ import unicode_literals
from django import forms
from definitions import models
from terms.models import Term



class AuthorsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthorsForm, self).__init__(*args, **kwargs)
    class Meta:
        model = models.Authors
        fields = ('in_text', 'citation', 'doi')
        labels = {
            'in_text': ('In Text Citation'),
            'citation': ('Full Citation'),
            'doi':('DOI')
        }

class DefinitionForm(forms.ModelForm):
    class Meta:
        fields = ('year', 'defs', 'discipline', 'synonym', 'citeNumber')
        labels = {
            'defs': ('Definition'),
            'citeNumber': ('Times Cited')
        }
        model = models.Definition


    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
