from app.models import UserRoleEnum

def load_function(user_role):
    if user_role == UserRoleEnum.Employee:
        return [
            {
                'name': 'Tiếp nhận học sinh',
                'url': '/admin'
            },
            {
                'name': 'Lập danh sách',
                'url': '/lapdanhsach'
            },
            {
                'name': 'Điều chỉnh danh sách',
                'url': '/dieuchinhdanhsach'
            },
        ]
    elif user_role == UserRoleEnum.Teacher:
        return [
            {
                'name': 'Điểm',
                'url': '/diem'
            }
        ]
    elif user_role == UserRoleEnum.Admin:
        return [
            {
                'name': 'Quy định',
                'url': '/quydinh'
            },
            {
                'name': 'Thống kê',
                'url': '/thongke'
            }
        ]
    return []

# read json and write json
