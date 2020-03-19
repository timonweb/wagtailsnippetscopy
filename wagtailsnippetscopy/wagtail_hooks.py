from wagtail.core import hooks

from .views import copy


@hooks.register('register_admin_urls')
def register_admin_urls():
    from django.conf.urls import url
    return [
        url(r'^snippets-copy/(\w+)/(\w+)/(\d+)/', copy, name='wagtailsnippetscopy_copy'),
    ]
