from flask import Blueprint
from flask_restx import Api
from flask_restx import Resource
from marshmallow import ValidationError

from flaskr.schema.toast import ToastSchema
from flaskr.service.toast import get_toasts_scalars
from flaskr.service.toast import get_toast_scalar
from flaskr.service.toast import add_new_toast
from flaskr.service.toast import delete_toast
from flaskr.service.toast import mark_read
from flaskr.service.toast import mark_read_all
from flaskr.view.toast_data import toast_post_data_schema
from flaskr.view.toast_data import toast_mark_read_all_data_schema


bp = Blueprint('toast', __name__, url_prefix="/toast")
api = Api(bp)


@api.route("/<id>")
class ToastResource(Resource):
    def get(self, id):
        schema = ToastSchema()
        scalar = get_toast_scalar(id)

        return schema.jsonify(scalar)

    def delete(self, id):
        try:
            delete_toast(id)
        except ValidationError as err:
            return {"validation": err.messages}, 400

        return {'id': id}


@api.route("/all")
class ToastsResource(Resource):
    def get(self):
        schema = ToastSchema(many=True)
        scalars = get_toasts_scalars()

        return schema.jsonify(scalars)


@api.route("/new")
class ToastNewResource(Resource):
    def post(self):
        try:
            post_data = toast_post_data_schema.load(api.payload)
        except ValidationError as err:
            return {"validation": err.messages}, 400

        new_toast = add_new_toast(post_data)
        schema = ToastSchema()

        return schema.jsonify(new_toast)


@api.route("/mark_read/<id>")
class ToastMarkReadResource(Resource):
    def put(self, id):
        try:
            toast = mark_read(id)
        except ValidationError as err:
            return {"validation": err.messages}, 400

        schema = ToastSchema()

        return schema.jsonify(toast)


@api.route("/mark_read_all")
class ToastsMarkReadResource(Resource):
    def put(self):
        try:
            mark_read_all_data = toast_mark_read_all_data_schema.load(api.payload)
            marked_count = mark_read_all(mark_read_all_data)
        except ValidationError as err:
            return {"validation": err.messages}, 400

        return {"marked_read": marked_count}
