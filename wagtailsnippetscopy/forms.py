from django import forms
from django.utils.translation import ugettext as _


class CopyForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.snippet = kwargs.pop('snippet')
        self.title_field_name = kwargs.pop('title_field_name')
        super(CopyForm, self).__init__(*args, **kwargs)
        self.fields['new_title'] = forms.CharField(initial=getattr(self.snippet, self.title_field_name),
                                                   label=_("New title"))

    def copy(self):
        new_snippet = self.snippet
        new_snippet.pk = None
        new_snippet.id = None
        setattr(new_snippet, self.title_field_name, self.cleaned_data.get('new_title'))
        new_snippet.save()
        return new_snippet
