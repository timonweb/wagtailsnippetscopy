from django.utils.safestring import mark_safe
from wagtail.contrib.modeladmin.options import ModelAdmin


def short(*args, **kwargs):
    print(kwargs)
    return 'SHORT'


class SnippetCopyModelAdminMixin(ModelAdmin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ['copy_snippet']
        self.copy_snippet.__func__.short_description = f'Copy {self.model._meta.verbose_name.title()}'

    def copy_snippet(self, obj):
        return mark_safe(f'<a href="{obj.get_snippet_copy_url()}">Copy</a>')
