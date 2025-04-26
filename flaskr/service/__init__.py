from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from flaskr.schema import Base


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
ma = Marshmallow()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
