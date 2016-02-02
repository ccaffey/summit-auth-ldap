from django.conf import settings
from django_auth_ldap.backend import LDAPBackend, _LDAPUser


class SummitLDAPBackend(LDAPBackend):
    def get_or_create_user(self, username, ldap_user):
        model = self.get_user_model()
        username_field = getattr(model, 'USERNAME_FIELD', 'username')
        try:
            email = ldap_user.attrs['mail'][0]
            kwargs = {username_field + '__iexact': email}
            return model.objects.get(**kwargs), False
        except (model.DoesNotExist, IndexError):
            pass

        kwargs = {
            username_field + '__iexact': username,
            'defaults': {username_field: username.lower()}
        }
        return model.objects.get_or_create(**kwargs)

    def django_to_ldap_username(self, username):
        return username.split('@')[0]


if settings.AUTH_LDAP_USER_DN_TEMPLATE and settings.AUTH_LDAP_USER_SEARCH:
    # monkey patch because our login DNs are have complicated structure and it's easier
    # to find real DN after authenticating with just username.
    _super_authenticate_user_dn = _LDAPUser._authenticate_user_dn

    def custom_authenticate_user_dn(self, password):
        _super_authenticate_user_dn(self, password)
        results = self.settings.USER_SEARCH.execute(
            self.connection, {'user': self._username})
        if results:
            self._user_dn = results[0][0]
            # self._user_attrs = results[0][1]

    _LDAPUser._authenticate_user_dn = custom_authenticate_user_dn
