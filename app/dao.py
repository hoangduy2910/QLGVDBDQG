import hashlib
from app import db
from app.models import *
from datetime import datetime, timedelta


# ADMIN
def check_login_admin(username, password):
    password = str(hashlib.md5(password.encode("utf-8")).hexdigest())
    user = User.query.filter(User.username == username.strip(),
                             User.password == password,
                             User.user_role == 2).first()

    return user


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
                             User.password == password,
                             User.user_role == 1).first()

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
def check_date_end_league(date_end):
    date_now = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_end = (date_end + timedelta(days=1)).strftime('%Y-%m-%d')

    if date_now <= date_end:
        return True

    return False


def create_league(name, address, image, gender_id, city_id, date_begin, date_end, user_id):
    league = League(name=name, address=address, image=image, gender_id=gender_id, city_id=city_id,
                    date_begin=date_begin, date_end=date_end, user_id=user_id)

    db.session.add(league)
    db.session.commit()

    return league


def update_league(league_id, name, address, image, gender_id, city_id, date_begin, date_end, user_id):
    league = League.query.get(league_id)

    league.name = name
    league.address = address
    league.image = image
    league.gender_id = gender_id
    league.city_id = city_id
    league.date_begin = date_begin
    league.date_end = date_end
    league.user_id = user_id

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


# CLUB
def create_club(name, phone, address, image, gender_id, level_id, user_id):
    club = Club(name=name, phone=phone, address=address, image=image,
                gender_id=gender_id, level_id=level_id, user_id=user_id)

    db.session.add(club)
    db.session.commit()


def read_clubs_by_user_id(user_id):
    return User.query.get(user_id).clubs


def read_club_by_id(club_id):
    return Club.query.get(club_id)


def read_club(keyword="", level_id=0, gender_id=0):
    clubs = Club.query

    if keyword:
        clubs = clubs.filter(Club.name.contains(keyword))

    if level_id:
        clubs = clubs.filter(Club.level_id == level_id)

    if gender_id:
        clubs = clubs.filter(Club.gender_id == gender_id)

    return clubs.all()


def read_club_by_league_id(league_id):
    pass


def update_club(user_id, name, phone, address, gender_id, level_id, image):
    club = Club.query.get(user_id)

    club.name = name
    club.phone = phone
    club.address = address
    club.gender_id = gender_id
    club.level_id = level_id
    club.image = image

    db.session.add(club)
    db.session.commit()


# LEAGUE CLUB
def get_club_id_in_league_club_by_league_id(league_id):
    clubs = []
    league_club = LeagueClub.query.filter(LeagueClub.league_id == league_id).all()
    for lc in league_club:
        clubs.append(lc.club_id)
    return clubs


def create_league_club(league_id, club_id, status_id):
    league_club = LeagueClub(league_id=league_id, club_id=club_id, status_id=status_id)

    db.session.add(league_club)
    db.session.commit()


def read_league_club_by_league_id(league_id):
    league_club = LeagueClub.query.filter(LeagueClub.league_id == league_id).all()
    return league_club


def update_status_club_in_league_club(league_id, club_id, status_id):
    league_club = LeagueClub.query.filter(LeagueClub.league_id == league_id, LeagueClub.club_id == club_id).first()
    league_club.status_id = status_id

    db.session.add(league_club)
    db.session.commit()


# STATUS
def read_status():
    return Status.query.all()


# CITY
def read_city():
    return City.query.all()


# LEVEL
def read_level():
    return Level.query.all()


# GENDER
def read_gender():
    return Gender.query.all()
