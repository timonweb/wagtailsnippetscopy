from django import forms
from django.db import models
from django.utils.translation import ugettext as _


class CopyFormBase(forms.Form):
    snippet = None
    title_field_name = None

    def __init__(self, *args, **kwargs):
        self.snippet = kwargs.pop('snippet')
        self.title_field_name = kwargs.pop('title_field_name')
        super().__init__(*args, **kwargs)

    def copy(self) -> models.Model:
        raise NotImplementedError(f'copy method is not defined')


class CopyForm(CopyFormBase):
    new_title = forms.CharField(label=_("New title"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_title'].initial = getattr(self.snippet, self.title_field_name)

    def copy(self):
        new_snippet = self.snippet
        new_snippet.pk = None
        new_snippet.id = None
        setattr(new_snippet, self.title_field_name, self.cleaned_data.get('new_title'))
        new_snippet.save()
        return new_snippet
