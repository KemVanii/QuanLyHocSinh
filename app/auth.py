from app.models import *
from flask_login import current_user
from functools import wraps
from flask import request, redirect, url_for


def restrict_to_roles(allowed_roles, next_url='index'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # check is login
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            # check role
            if current_user.user_role not in allowed_roles:
                return redirect(f"{url_for('login')}?next_url={next_url}")
            return f(*args, **kwargs)

        return decorated_function

    return decorator
