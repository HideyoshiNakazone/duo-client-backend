from duo.depends.depends_user import get_user_service
from duo.response.user.user_response import UserResponse
from duo.service.user_service import UserService
from duo.model.user_model import UserModel

from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends, Form
from fastapi_utils.cbv import cbv

from typing import Optional, Annotated


user_router = InferringRouter()


@cbv(user_router)
class UserController:
    user_service: UserService = Depends(get_user_service)

    @user_router.get("/user", status_code=200)
    def get_users(self, username: Optional[str] = None,
                  fullname: Optional[str] = None,
                  email: Optional[str] = None) -> list[UserModel]:
        return self.user_service.get_users(
            username=username,
            fullname=fullname,
            email=email
        )

    @user_router.post("/user/signup", status_code=201)
    def register(self, user_model: UserModel) -> UserResponse:
        return self.user_service.register(user_model)

    @user_router.post("/user/login", status_code=200)
    def login(self, username: Annotated[str, Form()], password: Annotated[str, Form()]) -> UserResponse:
        return self.user_service.login(username, password)

    @user_router.delete("/user/{user_id}", status_code=204)
    def remove(self, user_id: int):
        self.user_service.remove(user_id)

    @user_router.put("/user/{user_id}", status_code=204)
    def update_user(self, user_id: int, user_model: UserModel):
        self.user_service.update(user_id, user_model)
