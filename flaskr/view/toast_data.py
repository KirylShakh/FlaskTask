from dataclasses import dataclass
from dataclasses import field

from marshmallow import ValidationError
from marshmallow_dataclass import class_schema

from flaskr.service.user import get_user_scalar


def validate_user_id(user_id):
    if user_id is -1:
        return

    user = get_user_scalar(user_id)
    if user is None:
        raise ValidationError(f"No user with id {user_id} exists. Pass -1 for system toast")


@dataclass
class ToastPostData:
    body: str = field(metadata={"required": True})
    user_id: int = field(metadata={"validate": validate_user_id})


@dataclass
class ToastMarkReadAllData:
    user_id: int = field(metadata={"validate": validate_user_id})


toast_post_data_schema = class_schema(ToastPostData)()
toast_mark_read_all_data_schema = class_schema(ToastMarkReadAllData)()
