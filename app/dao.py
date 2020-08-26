import hashlib
from app import db
from app.models import *


def check_username(username):
    if User.query.filter_by(username=username).first():
        return True
    else:
        return False


def check_password(password, confirm):
    if password.strip() != confirm.strip():
        return True
    else:
        return False


def add_user(name, username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    user = User(name=name, username=username, password=password)

    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    user = User.query.filter_by(username=username).first()

    if user:
        password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
        if user.password == password:
            return user
        else:
            return False
    else:
        return False

