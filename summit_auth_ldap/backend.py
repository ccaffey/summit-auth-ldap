from django_auth_ldap.backend import LDAPBackend, LDAPUser, LDAPUserGroups


class SummitLDAPUser(LDAPUser):
    def _authenticate_user_dn(self, password):
        # because our login DNs are have complicated structure and it's easier
        # to find real DN after authenticating with just username.
        super(SummitLDAPUser, self)._authenticate_user_dn(password)
        if self.settings.USER_DN_TEMPLATE and self.settings.USER_SEARCH:
            results = self.settings.USER_SEARCH.execute(
                self.connection, {'user': self._username})
            if results:
                self._user_dn = results[0][0]


class SummitLDAPGroups(LDAPUserGroups):
    def is_member_of(self, group_dn):
        # allow REQUIRE_GROUP and DENY_GROUP to be lists of groups
        if isinstance(group_dn, (tuple, list, set)):
            return any(super(SummitLDAPGroups, self).is_member_of(group)
                       for group in group_dn)
        return super(SummitLDAPGroups, self).is_member_of(group_dn)


class SummitLDAPBackend(LDAPBackend):
    ldap_user_class = SummitLDAPUser
    ldap_groups_class = SummitLDAPGroups

    def get_or_create_user(self, username, ldap_user):
        model = self.get_user_model()
        username_field = getattr(model, 'USERNAME_FIELD', 'username')

        try:
            email = ldap_user.attrs['mail'][0]
        except (IndexError, KeyError):
            pass
        else:
            try:
                return model.objects.get(**{username_field + '__iexact': email}), False
            except (model.DoesNotExist, IndexError):
                pass

        kwargs = {
            username_field + '__iexact': username,
            'defaults': {username_field: username.lower()}
        }
        return model.objects.get_or_create(**kwargs)

    def django_to_ldap_username(self, username):
        return username.split('@')[0]
