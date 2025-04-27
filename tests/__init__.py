from logging import getLogger

from pytest import fixture

from flaskr import create_app
from flaskr.service import db
from flaskr.schema.toast import Toast

logger = getLogger(__name__)

@fixture()
def app():
    app = create_app({
        "TESTING": True
        , "SQLALCHEMY_DATABASE_URI": 'sqlite:///test_app.db'
    })

    yield app

    with app.app_context():
        num_rows_deleted = db.session.query(Toast).delete()
        db.session.commit()

    logger.info(f"removed {num_rows_deleted} toasts")

@fixture()
def client(app):
    return app.test_client()
