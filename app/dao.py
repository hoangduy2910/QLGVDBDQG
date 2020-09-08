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


def get_user_by_club_id(club_id):
    club = Club.query.get(club_id)
    return User.query.get(club.user_id)


# LEAGUE
def check_date_end_league(date_end):
    date_now = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_end = (date_end + timedelta(days=1)).strftime('%Y-%m-%d')

    if date_now <= date_end:
        return True

    return False


def create_league(name, address, image, gender_id, city_id, date_begin, date_end, user_id, has_scheduled):
    league = League(name=name, address=address, image=image, gender_id=gender_id, city_id=city_id,
                    date_begin=date_begin, date_end=date_end, user_id=user_id, has_scheduled=has_scheduled)

    db.session.add(league)
    db.session.commit()

    return league


def update_league(league_id, name, address, image, gender_id, city_id, date_begin, date_end, user_id, has_scheduled):
    league = League.query.get(league_id)

    league.name = name
    league.address = address
    league.image = image
    league.gender_id = gender_id
    league.city_id = city_id
    league.date_begin = date_begin
    league.date_end = date_end
    league.user_id = user_id
    league.has_scheduled = has_scheduled

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
    return Club.query.join(LeagueClub, Club.id == LeagueClub.club_id)\
        .filter(LeagueClub.league_id == league_id, LeagueClub.status_id == 2).all()


def read_club_name_by_club_id(club_id):
    return Club.query.get(club_id).name


def update_club(club_id, name, phone, address, image, gender_id, level_id, user_id):
    club = Club.query.get(club_id)

    club.name = name
    club.phone = phone
    club.image = image
    club.address = address
    club.gender_id = gender_id
    club.level_id = level_id
    club.user_id = user_id

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
    return LeagueClub.query.filter(LeagueClub.league_id == league_id).all()


def update_status_club_in_league_club(league_id, club_id, status_id):
    league_club = LeagueClub.query.filter(LeagueClub.league_id == league_id, LeagueClub.club_id == club_id).first()
    league_club.status_id = status_id

    db.session.add(league_club)
    db.session.commit()


def read_club_in_league_club(club_id):
    return LeagueClub.query.filter(LeagueClub.club_id == club_id,
                                   LeagueClub.status_id == 2).all()


# ROUND
def create_balanced_round_robin(league_id, clubs):
    rounds = Round.query.filter(Round.league_id == league_id).all()
    for r in rounds:
        db.session.delete(r)
        db.session.commit()

    schedule = []
    if len(clubs) % 2 == 1:
        clubs = clubs + [None]
    n = len(clubs)
    map = list(range(n))
    mid = n // 2
    for i in range(n-1):
        l1 = map[:mid]
        l2 = map[mid:]
        l2.reverse()
        round = []
        for j in range(mid):
            t1 = clubs[l1[j]]
            t2 = clubs[l2[j]]
            if j == 0 and i % 2 == 1:
                round.append((t2, t1))
            else:
                round.append((t1, t2))
        schedule.append(round)
        map = map[mid:-1] + map[:mid] + map[-1:]


    # Tạo vòng đấu
    for idx, rounds in enumerate(schedule):
        r = Round(name=str(idx+1), league_id=league_id)
        db.session.add(r)
        db.session.commit()

    # Tạo trận đấu thuộc vòng đấu
    for idx, round in enumerate(schedule):
        for match in round:
            if match[0] and match[1]:
                m = Match(home=match[0].id, away=match[1].id, date=None, round_id=idx+1, league_id=league_id)
                db.session.add(m)
                db.session.commit()

    # Tạo kết quả của mỗi trận đấu
    matches = read_match_by_league_id(league_id=league_id)
    for match in matches:
        home_result = Result(league_id=match.league_id, match_id=match.id, club_id=match.home,
                             type_result_id=None, score=0)
        away_result = Result(league_id=match.league_id, match_id=match.id, club_id=match.away,
                             type_result_id=None, score=0)

        db.session.add(home_result)
        db.session.add(away_result)
        db.session.commit()

    return schedule


# MATCH
def read_match_by_league_id(league_id):
    return Match.query.filter(Match.league_id == league_id).all()


def read_match_by_match_id(match_id):
    return Match.query.get(match_id)


def update_date_match(match_id, date, time):
    m = Match.query.get(match_id)
    m.date = datetime.strptime(date, '%Y-%m-%d')
    m.time = time

    db.session.add(m)
    db.session.commit()


# RESULT
def update_result_score_match(league_id, match_id, home_id, home_score, away_id, away_score):
    home_result = Result.query.filter(Result.league_id == league_id,
                                      Result.match_id == match_id,
                                      Result.club_id == home_id).first()
    away_result = Result.query.filter(Result.league_id == league_id,
                                      Result.match_id == match_id,
                                      Result.club_id == away_id).first()

    # 1-Thắng 2-Hòa 3-Thua
    if home_score > away_score:
        home_result.type_result_id = 1
        away_result.type_result_id = 3
    elif home_score == away_score:
        home_result.type_result_id = 2
        away_result.type_result_id = 2
    else:
        home_result.type_result_id = 3
        away_result.type_result_id = 1

    home_result.score = home_score
    away_result.score = away_score

    db.session.add(home_result)
    db.session.commit()

    db.session.add(away_result)
    db.session.commit()


def get_score_by_league_club_match(league_id, match_id, club_id):
    return Result.query.filter(Result.league_id == league_id,
                               Result.match_id == match_id,
                               Result.club_id == club_id).first().score


def get_goal_difference_by_league_club(league_id, club_id):
    score_win = 0
    score_lose = 0

    matches_home = Match.query.filter(Match.league_id == league_id, Match.home == club_id).all()
    for match in matches_home:
        result_home = Result.query.filter(Result.league_id == league_id,
                                          Result.match_id == match.id,
                                          Result.club_id == match.home).first()
        result_away = Result.query.filter(Result.league_id == league_id,
                                          Result.match_id == match.id,
                                          Result.club_id == match.away).first()
        if result_home.score > result_away.score:
            score_win = score_win + (result_home.score - result_away.score)
        elif result_home.score < result_home.score:
            score_lose = score_lose + (result_home.score - result_away.score)

    matches_away = Match.query.filter(Match.league_id == league_id, Match.away == club_id).all()
    for match in matches_away:
        result_away = Result.query.filter(Result.league_id == league_id,
                                          Result.match_id == match.id,
                                          Result.club_id == match.away).first()
        result_home = Result.query.filter(Result.league_id == league_id,
                                          Result.match_id == match.id,
                                          Result.club_id == match.home).first()

        if result_away.score > result_home.score:
            score_win = score_win + (result_away.score - result_home.score)
        elif result_away.score < result_home.score:
            score_lose = score_lose + (result_away.score - result_home.score)

    goal_difference = score_win + score_lose
    return goal_difference


def get_point_league_club(league_id, club_id):
    results = Result.query.filter(Result.league_id == league_id,
                                  Result.club_id == club_id).all()

    point = 0
    for result in results:
        if result.type_result_id == 1:
            point = point + 3
        elif result.type_result_id == 2:
            point = point + 1

    return point


def read_league_club_by_rank(league_id):
    clubs = []
    league_club = LeagueClub.query.filter(LeagueClub.league_id == league_id).all()
    for lc in league_club:
        if lc.status_id == 2:
            goal_difference = get_goal_difference_by_league_club(league_id=league_id, club_id=lc.club_id)
            point = get_point_league_club(league_id=league_id, club_id=lc.club_id)
            club = {
                'club_id': lc.club_id,
                'goal_difference': goal_difference,
                'point': point
            }
            clubs.append(club)

    rank = sorted(
        clubs,
        key=lambda c: (c['point'], c['goal_difference']),
        reverse=True
    )

    for idx, r in enumerate(rank):
        r['rank'] = idx + 1
        r['league_id'] = league_id

    return rank


# PLAYER
def create_player(name, birthday, phone, image, type_player_id, club_id):
    player = Player(name=name, birthday=birthday, phone=phone, image=image,
                    type_player_id=type_player_id, club_id=club_id)

    db.session.add(player)
    db.session.commit()


def update_player(player_id, name, birthday, phone, image, type_player_id, club_id):
    player = Player.query.get(player_id)

    player.name = name
    player.birthday = birthday
    player.phone = phone
    player.image = image
    player.type_player_id = type_player_id
    player.club_id = club_id

    db.session.add(player)
    db.session.commit()


def read_player_by_player_id(player_id):
    return Player.query.get(player_id)


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


# TYPE PLAYER
def read_type_player():
    return TypePlayer.query.all()
