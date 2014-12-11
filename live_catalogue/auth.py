from functools import partial

from django.conf import settings
from django.shortcuts import render

from live_catalogue.definitions import ADMIN_ROLES, ADMIN_GROUPS


def _get_user_roles(request):
    """ Roles are currently saved as django.auth groups by eea.frame
    """
    if request.user.is_authenticated():
        roles = [g.name for g in request.user.groups.all()]
    else:
        roles = []
    return request.user_roles + roles


def _has_perm(user_roles, user_groups, roles, groups):
    for user_role in user_roles:
        if user_role in roles:
            return True
    for user_group in user_groups:
        if user_group[0] in groups:
            return True
    return False


def _user_id(request):
    if request.user.is_authenticated():
        return request.user.username
    return request.user_id


class PermissionRequiredMixin(object):
    roles_required = []
    groups_required = []

    def dispatch(self, request, *args, **kwargs):
        dispatch = partial(super(PermissionRequiredMixin, self).dispatch,
                           request, *args, **kwargs)

        if getattr(settings, 'SKIP_AUTHORIZATION', False):
            return dispatch()

        user_roles = _get_user_roles(request)
        if not _has_perm(user_roles, request.user_groups,
                         self.roles_required, self.groups_required):
            return render(request, 'restricted.html')

        return dispatch()

    def user_id(self, request):
        return _user_id(request)


def is_admin(request):
    user_roles, user_groups = _get_user_roles(request), request.user_groups
    return _has_perm(user_roles, user_groups, ADMIN_ROLES, ADMIN_GROUPS)
