from marshmallow import ValidationError

from flaskr.service import db
from flaskr.schema.toast import Toast
from flaskr.schema.toast import Status


def get_toasts_scalars():
    return db.session.execute(db.select(Toast)).scalars()


def get_toast_scalar(id):
    return db.session.execute(db.select(Toast).where(Toast.id.is_(id))).scalar()


def get_toasts_for_user(user_id):
    return db.session.execute(db.select(Toast).where(Toast.user_id.is_(user_id))).scalars()


def add_new_toast(toast_data):
    new_toast = Toast()
    new_toast.body = toast_data.body
    new_toast.user_id = toast_data.user_id

    db.session.add(new_toast)
    db.session.commit()

    return new_toast


def mark_read(id):
    row = db.session.execute(db.select(Toast).where(Toast.id.is_(id))).first()
    
    if row is None:
        raise ValidationError(f"No toast present with id {id}")

    toast = row.Toast
    if toast.status is Status.READ:
        raise ValidationError(f"Toast {id} is already marked as read")

    toast.status = Status.READ
    toast.verified = True

    db.session.commit()

    return toast


def mark_read_all(toast_user_id_data):
    user_id = toast_user_id_data.user_id
    rows = db.session.execute(db.select(Toast).where(Toast.user_id.is_(user_id))).all()
    
    if len(rows) == 0:
        if user_id > 0:
            raise ValidationError(f"No toasts present for user with id {id}")
        elif user_id == -1:
            raise ValidationError(f"No system toasts present")
        else:
            raise ValidationError(f"Invalid user id {id}")

    count = 0
    for row in rows:
        toast = row.Toast
        if toast.status is Status.READ:
            continue

        count += 1
        toast.status = Status.READ
        toast.verified = True

    db.session.commit()

    return count


def delete_toast(id):
    row = db.session.execute(db.select(Toast).where(Toast.id.is_(id))).first()
    
    if row is None:
        raise ValidationError(f"No toast present with id {id}")

    db.session.delete(row.Toast)
    db.session.commit()
