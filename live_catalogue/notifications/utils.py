import ldap
from django.conf import settings
from live_catalogue.utils import cached


class LdapConnection(object):

    def __init__(self, data):
        ldap_server = data['LDAP_SERVER']
        if ldap_server is None:
            self.conn = None
        else:
            self.conn = ldap.initialize(ldap_server)
            self.conn.protocol_version = ldap.VERSION3
            self.conn.timeout = data['LDAP_TIMEOUT']
            self._user_dn_pattern = data['LDAP_USER_DN_PATTERN']

    def get_user_dn(self, user_id):
        return self._user_dn_pattern.format(user_id=user_id)

    def bind(self, user_id, password):
        if self.conn is None:
            return False
        user_dn = self.get_user_dn(user_id)
        try:
            result = self.conn.simple_bind_s(user_dn, password)
        except (ldap.INVALID_CREDENTIALS, ldap.UNWILLING_TO_PERFORM):
            return False
        assert result[:2] == (ldap.RES_BIND, [])
        return True

    def get_user_name(self, user_id):
        if self.conn is None:
            return u""
        user_dn = self.get_user_dn(user_id)
        result2 = self.conn.search_s(user_dn, ldap.SCOPE_BASE)
        [[_dn, attr]] = result2
        return attr['cn'][0].decode('utf-8')

    def get_user_email(self, user_id):
        if self.conn is None:
            return u""
        user_dn = self.get_user_dn(user_id)
        result2 = self.conn.search_s(user_dn, ldap.SCOPE_BASE)
        [[_dn, attr]] = result2
        return attr['mail'][0].lower()


@cached(86400)
def get_user_email(user_id):
    return LdapConnection(settings.LDAP_DATA).get_user_email(user_id)


@cached(86400)
def get_user_name(user_id):
    return LdapConnection(settings.LDAP_DATA).get_user_name(user_id)
