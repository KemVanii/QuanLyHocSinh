from flask_admin import Admin
from app import app, db
from flask_admin.contrib.sqla import ModelView
from app.models import Student, UserRoleEnum

admin = Admin(app=app, name='Tiếp nhận Học Sinh', template_mode='bootstrap4')


class MyStudent(ModelView):
    column_searchable_list = ['name', 'id']
    column_editable_list = ['name', 'dob', 'address', 'gender']
    edit_modal = True


admin.add_view(MyStudent(Student, db.session))
