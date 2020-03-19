from wagtailsnippetscopy.forms import CopyForm

default_meta = {
    'title_field_name': 'title',
    'copy_form_class': CopyForm
}


class Registry:

    def __init__(self):
        self._registry = {}

    def get(self, app_label, model_name):
        return self._registry.get(app_label, {}).get(model_name, None)

    def register(self, klass, meta=None):
        if meta is None:
            meta = {}
        meta = {**default_meta, **meta}
        self._registry.setdefault(klass._meta.app_label, {})[klass._meta.model_name] = meta


snippet_copy_registry = Registry()
