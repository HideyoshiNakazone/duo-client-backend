from duo.enum.roles_enum import RoleEnum
from duo.shared.entity import Entity

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, String


class UserEntity(Entity):
    __tablename__ = 'user'

    fullname = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    _roles = Column('roles', String(20), server_default='USER', nullable=False)

    @hybrid_property
    def roles(self) -> list[RoleEnum]:
        return [RoleEnum(role) for role in self._roles.split('$')]

    @roles.setter
    def roles(self, roles: list[RoleEnum]):
        self._roles = '$'.join([role.value for role in roles])

    def __repr__(self):
        return self._repr(
            id=self.id,
            username=self.username,
            fullname=self.fullname,
            email=self.email
        )
