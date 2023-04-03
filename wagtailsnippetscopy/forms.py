from django import forms
from django.db import models
from modelcluster.models import get_all_child_relations

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _


class CopyFormBase(forms.Form):
    snippet = None
    title_field_name = None
    title_field_label = None

    def __init__(self, *args, **kwargs):
        self.snippet = kwargs.pop('snippet')
        self.title_field_name = kwargs.pop('title_field_name')
        self.title_field_label = kwargs.pop('title_field_label')
        super().__init__(*args, **kwargs)

    def copy(self) -> models.Model:
        raise NotImplementedError(f'copy method is not defined')


class CopyForm(CopyFormBase):
    new_title = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_title'].initial = getattr(self.snippet, self.title_field_name)

        if self.title_field_label:
            self.fields['new_title'].label = _(self.title_field_label)

    def copy(self):
        # get all child relations
        relations = get_all_child_relations(self.snippet)
        relations_dict = {}
        for relation in relations:
            related_name = relation.related_name
            rels = getattr(self.snippet, related_name).all()
            relations_dict[related_name] = rels

        new_snippet = self.snippet
        new_snippet.pk = None
        new_snippet.id = None

        for key, values in relations_dict.items():
            new_values = []
            for value in values:
                new_val = value
                new_val.pk = None
                new_val.id = None
                new_values.append(new_val)
            setattr(new_snippet, key, new_values)

        setattr(new_snippet, self.title_field_name, self.cleaned_data.get('new_title'))

        new_snippet.save()
        return new_snippet
