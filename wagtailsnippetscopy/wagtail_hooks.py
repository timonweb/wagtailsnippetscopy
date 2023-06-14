try:
    from wagtail import hooks
except ImportError:
    from wagtail.core import hooks

from .views import copy


@hooks.register('register_admin_urls')
def register_admin_urls():
    try:
        from django.conf.urls import url
    except ImportError:
        from django.urls import re_path as url

    return [
        url(r'^snippets-copy/(\w+)/(\w+)/(\d+)/', copy, name='wagtailsnippetscopy_copy'),
    ]
