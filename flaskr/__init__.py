import os

from flask import Flask

from flaskr.service import init_db
from flaskr.view import user
from flaskr.view import toast


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
        , JSON_SORT_KEYS=False
        , SQLALCHEMY_DATABASE_URI='sqlite:///app.db'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_db(app)

    app.register_blueprint(user.bp)
    app.register_blueprint(toast.bp)

    return app


from flaskr.view import toast
