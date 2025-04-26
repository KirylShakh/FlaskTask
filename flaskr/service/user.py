from flaskr.service import db
from flaskr.schema.user import User


def get_users_scalars():
    return db.session.execute(db.select(User)).scalars()

def get_user_scalar(id):
    return db.session.execute(db.select(User).where(User.id.is_(id))).scalar()
