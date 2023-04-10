from duo.entity.user_entity import UserEntity

from passlib.hash import sha256_crypt
from dataclasses import dataclass

from typing import Optional, Union


@dataclass
class UserModel:
    username: str
    fullname: str
    email: str
    password: str | None

    id: Optional[int] = None

    def __post_init__(self):
        self.__password_hash()

    def __password_hash(self) -> None:
        if self.password is None:
            return

        if not sha256_crypt.identify(self.password.encode()):
            self.password = sha256_crypt.hash(self.password.encode())

    def verify_password(self, password: str) -> bool:
        return sha256_crypt.verify(password, self.password)

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            fullname=self.fullname,
            email=self.email,
            password=self.password
        )

    def update(self, user_model: 'UserModel') -> None:
        self.username = user_model.username
        self.fullname = user_model.fullname
        self.email = user_model.email

    def to_response(self) -> 'UserModel':
        self.password = None
        return self

    @classmethod
    def from_entity(cls, user_entity: UserEntity) -> Union['UserModel', None]:
        if user_entity is None:
            return None
        return cls(
            id=user_entity.id,
            username=user_entity.username,
            fullname=user_entity.fullname,
            email=user_entity.email,
            password=user_entity.password
        )
