from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.admin.utils import quote
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from wagtail.contrib.modeladmin.helpers import AdminURLHelper
from wagtail.wagtailadmin import messages
from wagtail.wagtailadmin.utils import (
    user_has_any_page_permission, user_passes_test, permission_denied)
from wagtail.wagtailadmin.views.pages import get_valid_next_url_from_request
from wagtail.wagtailcore import hooks
from wagtail.wagtailsnippets.permissions import get_permission_name
from wagtail.wagtailsnippets.views.snippets import get_snippet_model_from_url_params

from .forms import CopyForm
from .registry import snippet_copy_registry


@user_passes_test(user_has_any_page_permission)
def copy(request, app_label, model_name, id):
    # Validate snippet has been registered and title_field is set.
    title_field_name = snippet_copy_registry.get(app_label, model_name)
    if title_field_name is None:
        raise Exception("This snippet isn't registered as copyable")

    model = get_snippet_model_from_url_params(app_label, model_name)

    permission = get_permission_name('change', model)
    if not request.user.has_perm(permission):
        return permission_denied(request)

    snippet = get_object_or_404(model, id=id)

    # Create the form
    form = CopyForm(request.POST or None, snippet=snippet, title_field_name=title_field_name)

    next_url = get_valid_next_url_from_request(request)

    for fn in hooks.get_hooks('before_copy_snippet'):
        result = fn(request, snippet)
        if hasattr(result, 'status_code'):
            return result

    # Check if user is submitting
    if request.method == 'POST':

        if form.is_valid():

            # Copy the snippet
            new_snippet = form.copy()

            # Give a success message back to the user
            messages.success(request, _("Snippet '{0}' copied.").format(snippet))

            for fn in hooks.get_hooks('after_copy_snippet'):
                result = fn(request, snippet, new_snippet)
                if hasattr(result, 'status_code'):
                    return result

            if next_url:
                return redirect(next_url)
            if 'wagtail.contrib.modeladmin' in settings.INSTALLED_APPS:
                url_helper = AdminURLHelper(new_snippet)
                return redirect(url_helper.get_action_url('edit', quote(new_snippet.pk)))

            return redirect('wagtailsnippets:edit', app_label, model_name, new_snippet.id)

    return render(request, 'wagtailsnippetscopy/copy.html', {
        'snippet': snippet,
        'app_label': app_label,
        'model_name': model_name,
        'form': form,
        'next': next_url,
    })
