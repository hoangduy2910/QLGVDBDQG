import hashlib
from app import db
from app.models import *


# ADMIN
def check_login_admin(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    user = User.query.filter(User.username == username.strip(),
                             User.password == password).first()

    if user.user_role == 2:
        return user
    else:
        return None


# USER
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


def check_login(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    user = User.query.filter(User.username == username.strip(),
                             User.password == password).first()

    return user if user else False


def add_user(name, username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    user = User(name=name, username=username, password=password)

    db.session.add(user)
    db.session.commit()


def update_profile(user_id, name, phone, birthday):
    user = User.query.get(user_id)

    user.name = name
    user.phone = phone
    user.birthday = birthday

    db.session.add(user)
    db.session.commit()


# LEAGUE
def create_league(name, address, image, gender_id, city_id, user_id):
    league = League(name=name, address=address, image=image,
                    gender_id=gender_id, city_id=city_id, user_id=user_id)

    db.session.add(league)
    db.session.commit()


def read_leagues_by_user_id(user_id):
    return User.query.get(user_id).leagues


def read_league_by_id(league_id):
    return League.query.get(league_id)


def read_league(keyword="", city_id=0):
    leagues = League.query

    if keyword:
        leagues = leagues.filter(League.name.contains(keyword))

    if city_id != 0:
        leagues = leagues.filter(League.city_id == city_id)

    return leagues.all()


# CITY
def read_city():
    return City.query.all()


# LEVEL
def read_level():
    return Level.query.all()


# GENDER
def read_gender():
    return Gender.query.all()
