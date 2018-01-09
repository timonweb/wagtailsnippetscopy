from django.urls import reverse
from django.utils.safestring import mark_safe


class SnippetCopyMixin:

    def get_copy_url(self):
        return reverse('wagtailsnippetscopy_copy', args=(
            self._meta.app_label,
            self._meta.model_name,
            self.pk
        )
                       )

    @property
    def copy_snippet(self):
        return mark_safe('<a href="{}">Copy</a>'.format(self.get_copy_url()))
