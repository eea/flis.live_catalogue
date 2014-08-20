from functools import wraps

from django.conf import settings
from django.shortcuts import render

from live_catalogue.definitions import (
    VIEW_ROLES,
    VIEW_GROUPS,
    EDIT_GROUPS,
    EDIT_ROLES,
    ADMIN_ROLES,
    ADMIN_GROUPS,
)


def _has_perm(user_roles, user_groups, roles, groups):
    for user_role in user_roles:
        if user_role in roles:
            return True
    for user_group in user_groups:
        if user_group[0] in groups:
            return True
    return False


def login_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not getattr(settings, 'SKIP_EDIT_AUTHORIZATION', False):
            user_id = request.user_id
            user_roles, user_groups = request.user_roles, request.user_groups
            roles, groups = VIEW_ROLES + EDIT_ROLES, VIEW_GROUPS + EDIT_GROUPS
            if user_id and _has_perm(user_roles, user_groups, roles, groups):
                pass
            else:
                return render(request, 'restricted.html')
        return f(request, *args, **kwargs)
    return wrapper


def edit_permission_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not getattr(settings, 'SKIP_EDIT_AUTHORIZATION', False):
            user_roles, user_groups = request.user_roles, request.user_groups
            roles, groups = EDIT_ROLES, EDIT_GROUPS
            if _has_perm(user_roles, user_groups, roles, groups):
                pass
            else:
                return render(request, 'restricted.html')
        return f(request, *args, **kwargs)
    return wrapper


def admin_permission_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not getattr(settings, 'SKIP_ADMIN_AUTHORIZATION', False):
            user_roles, user_groups = request.user_roles, request.user_groups
            roles, groups = ADMIN_ROLES, ADMIN_GROUPS
            if _has_perm(user_roles, user_groups, roles, groups):
                pass
            else:
                return render(request, 'restricted.html')
        return f(request, *args, **kwargs)
    return wrapper


def is_admin(request):
    user_roles, user_groups = request.user_roles, request.user_groups
    return _has_perm(user_roles, user_groups, ADMIN_ROLES, ADMIN_GROUPS)
