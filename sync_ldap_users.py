import os
import sys
import logging
import ldap
from django.contrib.auth.models import User
from django_auth_ldap.config import LDAPSearch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Girmiti.settings")
import django
django.setup()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def sync_ldap_users():
    ldap_server_uri = 'ldap://192.168.0.7:389'
    ldap_bind_dn = 'CN=LDAPUser,CN=Users,DC=girmiti,DC=in'
    ldap_bind_password = 'L6x7y8$321'
    ldap_connection = ldap.initialize(ldap_server_uri)
    ldap_connection.simple_bind_s(ldap_bind_dn, ldap_bind_password)

    ldap_search = LDAPSearch(
        "cn=Users,dc=girmiti,dc=in",
        ldap.SCOPE_SUBTREE, # type: ignore # type: ignore
        "(objectClass=user)"
    )

    ldap_users = ldap_connection.search_s(
        ldap_search.base_dn,
        ldap_search.scope,
        ldap_search.filterstr
    )

    for ldap_user in ldap_users:
        username_bytes = ldap_user[1].get("sAMAccountName", [""])[0]
        username = username_bytes.decode("utf-8") if username_bytes else ""

        first_name = ldap_user[1].get("givenName", [""])[0]
        last_name = ldap_user[1].get("sn", [""])[0]
        email_bytes = ldap_user[1].get("mail", [""])[0]
        email = email_bytes.decode("utf-8") if email_bytes else ""

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                password=None,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            logging.debug(f"User created: {username}")
        else:
            logging.debug(f"User already exists: {username}")

    ldap_connection.unbind()

if __name__ == '__main__':
    sync_ldap_users()