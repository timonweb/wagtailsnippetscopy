from django.urls import reverse


class SnippetCopyMixin:
    def get_snippet_copy_url(self):
        return reverse('wagtailsnippetscopy_copy', args=(
                self._meta.app_label,
                self._meta.model_name,
                self.pk
            )
        )

    def get_snippet_verbose_name(self):
        return self._meta.verbose_name.title()
