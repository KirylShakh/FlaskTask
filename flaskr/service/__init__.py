from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from flaskr.schema import Base


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
ma = Marshmallow()


def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
