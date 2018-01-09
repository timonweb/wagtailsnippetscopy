class Registry:

    def __init__(self):
        self._registry = {}

    def get(self, app_label, model_name):
        return self._registry.get(app_label, {}).get(model_name, None)

    def register(self, klass, title_field_name):
        self._registry.setdefault(klass._meta.app_label, {})[klass._meta.model_name] = title_field_name


snippet_copy_registry = Registry()
