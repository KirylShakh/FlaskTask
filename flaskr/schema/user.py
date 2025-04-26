from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from flaskr.schema import Base
from flaskr.service import ma


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
