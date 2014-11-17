# -*- coding: utf-8 -*-

VIEW_ROLES = (
    'Administrator',
    'Contributor',
)
EDIT_ROLES = (
    'Administrator',
    'Contributor',
)
ADMIN_ROLES = (
    'Administrator',
)
VIEW_GROUPS = (
    'eionet-nfp',
)
EDIT_GROUPS = (
    'eionet-nrc-forwardlooking',
)
ADMIN_GROUPS = ()

ALL_ROLES = frozenset(VIEW_ROLES + EDIT_ROLES + ADMIN_ROLES)
ALL_GROUPS = frozenset(VIEW_GROUPS + EDIT_GROUPS + ADMIN_GROUPS)
