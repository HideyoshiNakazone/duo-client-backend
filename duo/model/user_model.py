from __future__ import annotations

from duo.entity.user_entity import UserEntity
from duo.enum.roles_enum import RoleEnum

from dataclasses import dataclass, field
from passlib.hash import sha256_crypt
from passlib.hash import pbkdf2_sha256

from typing import Optional, Union


@dataclass
class UserModel:
    username: str
    fullname: str
    email: str
    password: str | None

    roles: list[RoleEnum] = field(default_factory=lambda: [RoleEnum.USER])

    id: Optional[int] = None

    def __post_init__(self):
        self.__password_hash()

    def __password_hash(self) -> None:
        if self.password is None:
            return

        if not pbkdf2_sha256.identify(self.password.encode()):
            self.password = pbkdf2_sha256.hash(self.password.encode())

    def verify_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)

    def to_entity(self) -> UserEntity:
        user_entity = UserEntity(
            id=self.id,
            username=self.username,
            fullname=self.fullname,
            email=self.email,
            password=self.password
        )
        user_entity.roles = self.roles
        return user_entity

    def update(self, user_model: 'UserModel') -> None:
        self.username = user_model.username
        self.fullname = user_model.fullname
        self.email = user_model.email

    def to_response(self) -> 'UserModel':
        self.password = None
        return self

    @classmethod
    def from_entity(cls, user_entity: UserEntity) -> 'UserModel' | None:
        if user_entity is None:
            return None
        return cls(
            id=user_entity.id,
            username=user_entity.username,
            fullname=user_entity.fullname,
            email=user_entity.email,
            password=user_entity.password,
            roles=user_entity.roles
        )
