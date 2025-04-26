from flask import Blueprint

from flaskr.schema.user import UserSchema
from flaskr.service.user import get_users_scalars
from flaskr.service.user import get_user_scalar


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/")
def get_users():
    schema = UserSchema(many=True)
    scalars = get_users_scalars()

    return schema.jsonify(scalars)


@bp.route("/<id>")
def get_user(id):
    schema = UserSchema()
    scalar = get_user_scalar(id)

    return schema.jsonify(scalar)
