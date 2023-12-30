from app.models import UserRoleEnum

def load_function(user_role):
    match user_role:
        case UserRoleEnum.Employee:
            return [
                {
                    'name': 'Tiếp nhận học sinh',
                    'url': '/tiepnhanhocsinh'
                },
                {
                    'name': 'Lập danh sach',
                    'url': '/lapdanhsach'
                },
                {
                    'name': 'Điều chỉnh danh sách',
                    'url': '/dieuchinhdanhsach'
                },
            ]
        case UserRoleEnum.Teacher:
            return [
                {
                    'name': 'Điểm',
                    'url': '/diem'
                }
            ]
        case UserRoleEnum.Admin:
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
