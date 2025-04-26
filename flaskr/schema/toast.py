from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from flaskr.schema import Base
from flaskr.schema.user import UserSchema
from flaskr.service import ma


class Status(Enum):
    UNREAD = "unread"
    READ = "read"


class Toast(Base):
    __tablename__ = "toast"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[Status] = mapped_column(server_default=Status.UNREAD.name, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)


class ToastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Toast
        include_fk = True
        load_instance = True
