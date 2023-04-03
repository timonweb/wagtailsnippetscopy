from wagtail import hooks

from .views import copy


@hooks.register('register_admin_urls')
def register_admin_urls():
    try:
        from django.conf.urls import url
    except ImportError:
        from django.urls import re_path as url

    return [
        url(r'^snippets-copy/(\w+)/(\w+)/(\w+)/', copy, name='wagtailsnippetscopy_copy'),
    ]
