
from duo.shared.exception.invalid_user_authentication_exception import InvalidUserAuthenticationException
from duo.shared.exception.user_already_exists_exception import UserAlreadyExistsException
from duo.shared.exception.user_not_found_exception import UserNotFoundException
from duo.repo.user_repository import UserRepository
from duo.service.auth_service import AuthService
from duo.model.user_model import UserModel


class UserService:
    __slots__ = ['user_repo', 'auth_service']

    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def get_users(self, **kwargs) -> list[UserModel]:
        users = self.user_repo.get_all(**kwargs)
        return [UserModel.from_entity(user).to_response() for user in users]

    def login(self, username: str, password: str) -> UserModel:
        user = self.user_repo.get_user_by_username(username)
        if user is None:
            raise UserNotFoundException(
                "User not found."
                " Please try again with a valid user."
            )

        userData = UserModel.from_entity(user)
        if not userData.verify_password(password):
            raise InvalidUserAuthenticationException(
                "Invalid Credentials."
                " Please try again with a valid username and password."
            )

        return userData.to_response()

    def register(self, user_model: UserModel) -> UserModel:
        user = self.user_repo.get_user_by_username(user_model.username)
        if user is not None:
            raise UserAlreadyExistsException(
                "User already exists."
                " Please try again with a different username."
            )
        return UserModel.from_entity(self.user_repo.add(user_model.to_entity())) \
            .to_response()

    def remove(self, user_id: int) -> None:
        user = self.user_repo.get(user_id)
        if user is None:
            raise UserNotFoundException(
                "User not found."
                " Please try again with a valid user."
            )
        self.user_repo.remove(user)

    def update(self, user_id: int, user_model: UserModel) -> UserModel:
        user = UserModel.from_entity(self.user_repo.get(user_id))
        if user is None:
            raise UserNotFoundException(
                "User not found."
                " Please try again with a valid user."
            )

        user.update(user_model)

        return UserModel.from_entity(self.user_repo.update(user.to_entity())) \
            .to_response()
