from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, PasswordField, TextField
from wtforms.fields import DateField
from flask_login import current_user
from flask import flash
from sqlalchemy import inspect
from app.models import *
from app import app, db
from app.models import Subject
import hashlib
from datetime import datetime

admin = Admin(app=app, name='Admin', template_mode='bootstrap4', url="/")


class AuthenticatedEmployee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.Employee


class MyStudent(AuthenticatedEmployee):
    column_searchable_list = ['name', 'id']
    column_editable_list = ['name', 'dob', 'address', 'gender']
    edit_modal = True
    form_excluded_columns = ['score_boards', 'phones', 'status']
    form_extra_fields = {
        'name': TextField('Họ và tên:'),
        'gender': SelectField('Phái', choices=[(True, 'Nam'), (False, 'Nữ')], coerce=bool),
        'dob': DateField('Ngày sinh', format='%Y-%m-%d'),
        'isTransferSchool': SelectField('Loại tiếp nhận', choices=[(False, 'Chuyển cấp'), (True, 'Chuyển trường')], coerce=bool),
    }

    def validate_form(self, form):
        dob = form.dob.data
        if dob:
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            min_age = int(app.config['age_min'])
            max_age = int(app.config['age_max'])
            if age < min_age or age > max_age:
                flash(f"Tuổi phải nằm trong khoảng từ {min_age} đến {max_age}.", 'error')
                return False
        return super(MyStudent, self).validate_form(form)

    def delete_model(self, model):
        if model.status:
            model.status = False
            self.session.commit()
            flash('Dữ liệu đã được đánh dấu là không hoạt động.Bấm lại xóa để bật', 'success')
        else:
            model.status = True
            self.session.commit()
            flash('Dữ liệu đã được đánh dấu là hoạt động. Bấm lại xóa để tắt', 'success')
        return True


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.Admin


class MyUser(AuthenticatedAdmin):
    edit_modal = True
    column_filters = ['user_role']
    column_exclude_list = ['subject_id']
    column_list = [c_attr.key for c_attr in inspect(User).mapper.column_attrs]
    form_excluded_columns = ['phones']
    form_extra_fields = {
        'gender': SelectField('Gender', choices=[(True, 'Nam'), (False, 'Nữ')], coerce=bool)
    }

    def on_model_change(self, form, model, is_created):
        # Hash the password before saving to the database
        password = form.password.data
        password_form_hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
        if model.password != password:
            model.password = hashlib.md5(password.encode('utf-8')).hexdigest()

    def delete_model(self, model):
        if model.status:
            model.status = False
            self.session.commit()
            flash('Dữ liệu đã được đánh dấu là không hoạt động.Bấm lại xóa để bật', 'success')
        else:
            model.status = True
            self.session.commit()
            flash('Dữ liệu đã được đánh dấu là hoạt động. Bấm lại xóa để tắt', 'success')

        return True


class PhoneNumberView(AuthenticatedAdmin):
    edit_modal = True


class MySubject(AuthenticatedAdmin):
    edit_modal = True
    column_list = ['id', 'name', 'status']
    form_excluded_columns = ['score_boards', 'classes']

    def after_model_change(self, form, model, is_created):
        if is_created:
            flash('Hãy thêm giảng viên cho môn học vừa thêm', 'info')

    def delete_model(self, model):
        if hasattr(model, 'status'):
            if model.status:
                model.status = False
                self.session.commit()
                flash('Dữ liệu đã được đánh dấu là không hoạt động.Bấm lại xóa để bật', 'success')
            else:
                model.status = True
                self.session.commit()
                flash('Dữ liệu đã được đánh dấu là hoạt động. Bấm lại xóa để tắt', 'success')
        else:
            flash('Không thể tìm thấy cột status.', 'error')

        return True


admin.add_view(MyStudent(Student, db.session))
admin.add_view(MyUser(User, db.session))
admin.add_view(MySubject(Subject, db.session))
admin.add_view(PhoneNumberView(PhoneUser, db.session))
