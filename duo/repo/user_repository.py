from typing import Type

from duo.shared.repository import Repository
from duo.entity.user_entity import UserEntity

from sqlalchemy.orm import Session


class UserRepository(Repository):
    entity = UserEntity

    def get_user_by_username(self, username) -> UserEntity | None:
        with Session(self.engine) as session:
            return session.query(self.entity).filter_by(username=username).first()

    def get_user_by_fullname(self, fullname) -> UserEntity | None:
        with Session(self.engine) as session:
            return session.query(self.entity).filter_by(fullname=fullname).first()

    def get_user_by_email(self, email) -> UserEntity | None:
        with Session(self.engine) as session:
            return session.query(self.entity).filter_by(email=email).first()
