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


def read_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())

    user = User.query.filter(User.username == username.strip(),
                             User.password == password).first()

    return user if user else False


def read_city():
    return City.query.all()


def read_city_by_id(city_id):
    return City.query.get(city_id)


def read_level():
    return Level.query.all()


def read_gender():
    return Gender.query.all()


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


def update_profile(user_id, phone, birthday, name):
    user = User.query.get(user_id)

    user.name = name
    user.phone = phone
    user.birthday = birthday

    db.session.add(user)
    db.session.commit()



