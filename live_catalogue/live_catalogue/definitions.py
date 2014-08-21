# -*- coding: utf-8 -*-


COUNTRIES = (
    ('sq', 'Albania'),
    ('at', 'Austria'),
    ('be', 'Belgium'),
    ('ba', 'Bosnia and Herzegovina'),
    ('bg', 'Bulgaria'),
    ('hr', 'Croatia'),
    ('cy', 'Cyprus'),
    ('cz', 'Czech Republic'),
    ('dk', 'Denmark'),
    ('ee', 'Estonia'),
    ('fi', 'Finland'),
    ('fr', 'France'),
    ('de', 'Germany'),
    ('gr', 'Greece'),
    ('hu', 'Hungary'),
    ('is', 'Iceland'),
    ('ie', 'Ireland'),
    ('it', 'Italy'),
    ('xk', 'Kosovo under the UN SCR 1244/99'),
    ('lv', 'Latvia'),
    ('li', 'Liechtenstein'),
    ('lt', 'Lithuania'),
    ('lu', 'Luxembourg'),
    ('mk', 'Macedonia, FYR of'),
    ('mt', 'Malta'),
    ('me', 'Montenegro'),
    ('nl', 'Netherlands'),
    ('no', 'Norway'),
    ('pl', 'Poland'),
    ('pt', 'Portugal'),
    ('ro', 'Romania'),
    ('rs', 'Serbia'),
    ('sk', 'Slovakia'),
    ('si', 'Slovenia'),
    ('es', 'Spain'),
    ('se', 'Sweden'),
    ('ch', 'Switzerland'),
    ('tr', 'Turkey'),
    ('uk', 'United Kingdom'),
)

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
