from wagtail.contrib.modeladmin.options import ModelAdmin


class SnippetCopyModelAdminMixin(ModelAdmin):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = list(self.list_display) + ['copy_snippet'] \
            if self.list_display else 'copy_snippet'
