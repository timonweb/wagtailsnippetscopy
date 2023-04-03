# 'Copy A Snippet' Feature for Wagtail CMS

You can now "copy" snippets (non-page models) in Wagtail CMS

## Installation

1. Install the python package wagtailsnippetscopy from pip

`pip install wagtailsnippetscopy`

Alternatively, you can install download or clone this repo and call `pip install -e .`.

2. Add to INSTALLED_APPS in your **settings.py**:

`'wagtailsnippetscopy',`

3. Register a model (with a title field name) you wish to enable copy functionality for:

```python
from wagtailsnippetscopy.registry import snippet_copy_registry

snippet_copy_registry.register(YourModel, {})
```

4. Add SnippetCopyMixin to your Snippet model in order to enable get_copy_url callback() for the model:

```python
from wagtailsnippetscopy.models import SnippetCopyMixin
from wagtail.snippets.models import register_snippet

@register_snippet
class Graph(SnippetCopyMixin, models.Model):
```

In order for the `Copy` Button to appear in your Snippet list actions automatically, add the following to your app `wagtail_hooks.py`

```python
from wagtail import hooks
from wagtail.snippets import widgets as wagtailsnippets_widgets

@hooks.register('register_snippet_listing_buttons')
def snippet_listing_buttons(snippet, user, next_url=None):
    if hasattr(snippet, "get_snippet_copy_url"):
        url = snippet.get_snippet_copy_url()
        yield wagtailsnippets_widgets.SnippetListingButton(
            "Copy",
            url,
            priority=20
        )

```

Now if you go to your snippet list, you will see a new `Copy` button alongside `Edit` and `Delete`



5. If you wish copy link to automatically appear in modeladmin list you should add SnippetCopyModelAdminMixin to the ModelAdmin class:

In admin.py:

```python
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtailsnippetscopy.admin import SnippetCopyModelAdminMixin
from .models import YourModel

class YourModelAdmin(SnippetCopyModelAdminMixin, ModelAdmin):
    model = YourModel

modeladmin_register(GraphAdmin)
```

6. Copy link follows the following pattern:

```
/admin/copy-snippet/<app_label>/<model_name>/<object_id>/
```

## Bugs and suggestions

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

[https://github.com/timonweb/wagtailsnippetscopy/issues](https://github.com/timonweb/wagtailsnippetscopy/issues)

by [Tim Kamanin](https://timonweb.com/wagtail-developer/)
