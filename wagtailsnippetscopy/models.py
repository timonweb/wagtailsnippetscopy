from django.urls import reverse
import uuid


class SnippetCopyMixin:
    def get_snippet_copy_url(self):
        pk = self.pk

        if isinstance(pk, uuid.UUID):
            pk = self.pk.hex

        return reverse('wagtailsnippetscopy_copy', args=(
            self._meta.app_label,
            self._meta.model_name,
            pk
        )
                       )

    def get_snippet_verbose_name(self):
        return self._meta.verbose_name.title()
