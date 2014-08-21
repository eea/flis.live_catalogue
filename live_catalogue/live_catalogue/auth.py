from functools import partial

from django.conf import settings
from django.shortcuts import render

from live_catalogue.definitions import ADMIN_ROLES, ADMIN_GROUPS

def _has_perm(user_roles, user_groups, roles, groups):
    for user_role in user_roles:
        if user_role in roles:
            return True
    for user_group in user_groups:
        if user_group[0] in groups:
            return True
    return False


class PermissionRequiredMixin(object):

    roles_required = []
    groups_required = []

    def dispatch(self, request, *args, **kwargs):
        dispatch = partial(super(PermissionRequiredMixin, self).dispatch,
                           request, *args, **kwargs)

        if getattr(settings, 'SKIP_AUTHORIZATION', False):
            return dispatch()

        if not _has_perm(request.user_roles, request.user_groups,
                         self.roles_required, self.groups_required):
            return render(request, 'restricted.html')

        return dispatch()


def is_admin(request):
    user_roles, user_groups = request.user_roles, request.user_groups
    return _has_perm(user_roles, user_groups, ADMIN_ROLES, ADMIN_GROUPS)