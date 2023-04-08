from duo.depends.depends_user import get_user_service
from duo.service.user_service import UserService
from duo.model.user_model import UserModel

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi import Depends, Form

from typing import Optional, Annotated

user_router = InferringRouter()


@cbv(user_router)
class UserController:
    user_service: UserService = Depends(get_user_service)

    @user_router.get("/user")
    def get_users(self, username: Optional[str] = None,
                  fullname: Optional[str] = None,
                  email: Optional[str] = None) -> list[UserModel]:
        return self.user_service.get_users(
            username=username,
            fullname=fullname,
            email=email
        )

    @user_router.post("/user/signup")
    def register(self, user_model: UserModel) -> UserModel:
        return self.user_service.register(user_model)

    @user_router.post("/user/login")
    def login(self, username: Annotated[str, Form()], password: Annotated[str, Form()]) -> UserModel:
        print(username, password)

        return self.user_service.login(username, password)
