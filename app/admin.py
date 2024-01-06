from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy import inspect
from app.models import *
from app import app, db
from app.models import Subject
import hashlib

admin = Admin(app=app, name='Admin', template_mode='bootstrap4', url="/")


class AuthenticatedEmployee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.Employee


class MyStudent(AuthenticatedEmployee):
    column_searchable_list = ['name', 'id']
    column_editable_list = ['name', 'dob', 'address', 'gender']
    edit_modal = True


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.Admin


class MyUser(AuthenticatedAdmin):
    edit_modal = True
    column_hide_backrefs = False
    column_filters = ['user_role']
    column_list = [c_attr.key for c_attr in inspect(User).mapper.column_attrs]

    def on_model_change(self, form, model, is_created):
        # Hash the password before saving to the database
        if 'password' in form:
            password = form.password.data
            model.password = hashlib.md5(password.encode('utf-8')).hexdigest()


class MySubject(AuthenticatedAdmin):
    edit_modal = True

    def on_model_delete(self, model):
        new_parent = Subject.query.first()
        User.query.filter_by(subject_id=model.id).update({'subject_id': new_parent.id})
        db.session.commit()


admin.add_view(MyStudent(Student, db.session))
admin.add_view(MyUser(User, db.session))
admin.add_view(MySubject(Subject, db.session))
