from duo.shared.entity import Entity

from sqlalchemy import Column, String


class UserEntity(Entity):
    __tablename__ = 'user'

    fullname = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return self._repr(
            id=self.id,
            username=self.username,
            fullname=self.fullname,
            email=self.email
        )
