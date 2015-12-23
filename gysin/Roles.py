# -*- coding: utf-8 -*-
from flaskext.auth import Auth, AuthUser, Role, Permission

def auth_roles(app):
    auth = Auth(app, login_url_name="login")
    auth.user_timeout = app.config["USER_TIMEOUT"]

    # permission = Permission(resource, action)
    create_poem = Permission("create", "poem")
    administer_things = Permission("administer", "things")

    roles = {
            "user": Role("user", [create_poem]),
            "admin": Role("admin",
                [create_poem, administer_things])
            }
    
    def load_role(role_name):
        return roles.get(role_name)

    auth.load_role = load_role
    return auth
