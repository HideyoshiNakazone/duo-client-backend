from duo.depends.depends_user import get_user_service, load_default_admin_user
from duo.endpoints.user.model.user_model import UserModel
from duo.endpoints.user.entity.roles_enum import RoleEnum


def execute():

    default_user = UserModel(
        **load_default_admin_user(),
        roles=[RoleEnum.ADMIN, RoleEnum.USER]
    )

    user_service = get_user_service()
    if not user_service.get_users(username=default_user.username):
        user_service.register(default_user)
