from django.apps import apps
from django.conf import settings
from django.contrib.admin.utils import quote
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from wagtail.admin import messages
from wagtail.admin.auth import user_passes_test, user_has_any_page_permission, permission_denied
from wagtail.admin.views.pages import get_valid_next_url_from_request
from wagtail.contrib.modeladmin.helpers import AdminURLHelper
from wagtail.core import hooks
from wagtail.snippets.permissions import get_permission_name

from .registry import snippet_copy_registry


@user_passes_test(user_has_any_page_permission)
def copy(request, app_label, model_name, id):
    # Validate snippet has been registered and title_field is set.
    meta = snippet_copy_registry.get(app_label, model_name)
    if meta is None:
        raise Exception("This snippet isn't registered as copyable")

    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise Http404

    permission = get_permission_name('change', model)
    if not request.user.has_perm(permission):
        return permission_denied(request)

    snippet = get_object_or_404(model, id=id)

    # Create the form
    form = meta['copy_form_class'](request.POST or None, snippet=snippet, title_field_name=meta['title_field_name'])

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
            messages.success(request, _(f"{snippet.get_snippet_verbose_name()} '{snippet}' has been copied.").format(snippet))

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
