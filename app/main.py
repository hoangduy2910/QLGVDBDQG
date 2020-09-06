from app import app, dao, login
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta


@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# ADMIN
@app.route("/admin/login", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        err_msg = ""
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.check_login_admin(username=username, password=password)

        if user:
            login_user(user=user)
            return redirect("/admin")
        else:
            err_msg = "Tên tài khoản hoặc mật khẩu không hợp lệ."
    return redirect("/admin")


# USER
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/giai-dau")
def league():
    cities = dao.read_city()
    date_now = datetime.now()

    keyword = request.args["keyword"] if request.args.get("keyword") else ""
    city_id = request.args["city_id"] if request.args.get("city_id") else 0
    leagues = dao.read_league(keyword=keyword, city_id=int(city_id))

    return render_template("leagues.html", cities=cities, leagues=leagues,
                           keyword=keyword, city_id=int(city_id), date_now=date_now)


@app.route("/doi")
def club():
    levels = dao.read_level()
    genders = dao.read_gender()

    keyword = request.args["keyword"] if request.args.get("keyword") else ""
    level_id = request.args["level_id"] if request.args.get("level_id") else 0
    gender_id = request.args["gender_id"] if request.args.get("gender_id") else 0
    clubs = dao.read_club(keyword=keyword, level_id=int(level_id), gender_id=int(gender_id))

    return render_template("clubs.html", clubs=clubs, levels=levels, genders=genders,
                           level_id=level_id, gender_id=gender_id, keyword=keyword)


@app.route("/dang-nhap", methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.check_login(username=username, password=password)

        if user:
            login_user(user=user)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
        else:
            err_msg = "Tên tài khoản hoặc mật khẩu không hợp lệ."

    return render_template("login.html", err_msg=err_msg)


@app.route("/dang-ky", methods=["get", "post"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if dao.check_username(username=username):
            err_msg = "Tên tài khoản đã tồn tại."
        elif dao.check_password(password=password, confirm=confirm):
            err_msg = "Mật khẩu và mật khẩu xác nhận phải giống nhau."
        else:
            dao.add_user(name=name, username=username, password=password)
            return redirect(url_for('login'))
    return render_template("register.html", err_msg=err_msg)


@app.route("/dang-xuat")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/thong-tin-ca-nhan/<int:user_id>", methods=["get", "post"])
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    err_msg = ""

    if request.method == "POST":
        if request.form.get("name") and request.form.get("phone") and request.form.get("birthday"):
            name = request.form.get("name")
            phone = request.form.get("phone")
            birthday = request.form.get("birthday")

            dao.update_profile(user_id=user_id, name=name, phone=phone, birthday=birthday)
            msg = "Cập nhật thành công !"

            return render_template('profile.html', user=user, msg=msg)
        else:
            err_msg = "Bạn phải nhập đủ thông tin !"

    return render_template('profile.html', user=user, err_msg=err_msg)


@app.route("/quan-ly-giai-dau")
@login_required
def my_league():
    leagues = dao.read_leagues_by_user_id(current_user.id)
    return render_template('my-league.html', leagues=leagues, date_now=datetime.now())


@app.route("/quan-ly-doi-bong")
@login_required
def my_club():
    clubs = dao.read_clubs_by_user_id(current_user.id)
    genders = dao.read_gender()
    levels = dao.read_level()
    return render_template('my-club.html', clubs=clubs, genders=genders, levels=levels)


@app.route("/tao-doi", methods=["get", "post"])
@login_required
def create_club():
    levels = dao.read_level()
    genders = dao.read_gender()

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        image = ""
        gender_id = request.form.get("gender_id")
        level_id = request.form.get("level_id")
        user_id = current_user.id

        dao.create_club(name=name, phone=phone, address=address, image=image,
                        gender_id=int(gender_id), level_id=int(level_id), user_id=user_id)

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        return redirect(url_for('club_detail'))

    return render_template("create-club.html", levels=levels, genders=genders)


@app.route("/tao-giai-dau", methods=["get", "post"])
@login_required
def create_league():
    genders = dao.read_gender()
    cities = dao.read_city()
    date_now = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        image = ''
        gender_id = request.form.get("gender_id")
        city_id = request.form.get("city_id")
        date_begin = datetime.now()
        date_end = request.form.get("date_end")
        user_id = current_user.id
        has_scheduled = False

        league = dao.create_league(name=name, address=address, image=image,
                                   gender_id=int(gender_id), city_id=int(city_id),
                                   date_begin=date_begin, date_end=date_end,
                                   user_id=int(user_id), has_scheduled=has_scheduled)

        return redirect(url_for('register_league', league_id=league.id))

    return render_template("create-league.html", genders=genders, cities=cities,
                           date_now=date_now)


@app.route("/chi-tiet-doi-bong")
def club_detail():
    return render_template('club-detail.html')


@app.route("/cau-thu-cua-doi")
def players_club():
    return render_template('players-club.html')


@app.route("/giai-dau-cua-doi")
def leagues_club():
    return render_template('leagues-club.html')


@app.route("/thanh-tich-cua-doi")
def achievements():
    return render_template('achievements.html')


@app.route("/chi-tiet-cau-thu")
def player_detail():
    return render_template('player-detail.html')


@app.route("/dang-ky-thi-dau/<int:league_id>", methods=["get", "post"])
def register_league(league_id):
    cities = dao.read_city()
    league = dao.read_league_by_id(league_id)
    league_club = dao.get_club_id_in_league_club_by_league_id(league_id)

    check_date = False
    date_now = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_end = (league.date_end + timedelta(days=1)).strftime('%Y-%m-%d')

    if date_now <= date_end:
        check_date = True

    if request.method == "POST":
        league_id = league_id
        club_id = request.form.get("club_id")
        status_id = 1

        dao.create_league_club(league_id=league_id, club_id=int(club_id), status_id=status_id)

        return redirect(url_for('register_league', league_id=league_id))

    return render_template('register-league.html', league=league, cities=cities, date_now=date_now,
                           date_end=date_end, check_date=check_date, league_club=league_club)


@app.route("/lich-thi-dau/<int:league_id>", methods=["get", "post"])
def schedule(league_id):
    league = dao.read_league_by_id(league_id)
    cities = dao.read_city()
    clubs = dao.read_club_by_league_id(league_id)
    check_date = dao.check_date_end_league(league.date_end)
    date_now = datetime.now()
    msg = ""

    if request.method == "POST":
        if not league.has_scheduled:
            dao.create_balanced_round_robin(league_id=league_id, clubs=clubs)
            dao.update_league(league_id=league.id, name=league.name, address=league.address,
                              image=league.image, gender_id=league.gender_id,
                              city_id=league.city_id, date_begin=league.date_begin,
                              date_end=(date_now - timedelta(days=1)), user_id=league.user_id, has_scheduled=True)

            return redirect(url_for('schedule', league_id=league_id))
        else:
            msg = "Giải đấu đã có lịch thi đấu !"

    return render_template('schedule.html', league=league, cities=cities, check_date=check_date,
                           msg=msg, date_now=date_now.strftime("%Y-%m-%d"))


@app.route("/xep-hang/<int:league_id>")
def rank(league_id):
    cities = dao.read_city()
    league = dao.read_league_by_id(league_id)
    check_date = dao.check_date_end_league(league.date_end)

    league_club = dao.read_league_club_by_league_id(league_id=league_id)

    return render_template('rank.html', league=league, cities=cities, check_date=check_date, league_club=league_club)


@app.route("/cac-doi-cua-giai-dau/<int:league_id>")
def clubs_league(league_id):
    cities = dao.read_city()
    league = dao.read_league_by_id(league_id)
    check_date = dao.check_date_end_league(league.date_end)

    league_club = dao.read_league_club_by_league_id(league_id=league_id)

    return render_template('clubs-league.html', league=league, cities=cities,
                           check_date=check_date, league_club=league_club)


@app.route("/danh-sach-dang-ky/<int:league_id>")
@login_required
def list_register(league_id):
    league = dao.read_league_by_id(league_id)
    cities = dao.read_city()
    status = dao.read_status()
    check_date = dao.check_date_end_league(league.date_end)

    league_club = dao.read_league_club_by_league_id(league_id=league_id)

    if request.args.get('status_id') and request.args.get('club_id'):
        status_id = request.args.get('status_id')
        club_id = request.args.get('club_id')

        dao.update_status_club_in_league_club(league_id=league_id, club_id=int(club_id), status_id=int(status_id))

        return redirect(url_for('list_register', league_id=league_id))

    return render_template('list-register.html', league=league, cities=cities, status=status,
                           check_date=check_date, league_club=league_club)


@app.route("/tuy-chinh-giai-dau/<int:league_id>", methods=["get", "post"])
@login_required
def settings(league_id):
    cities = dao.read_city()
    genders = dao.read_gender()
    league = dao.read_league_by_id(league_id)
    date_now = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    check_date = dao.check_date_end_league(league.date_end)

    err_msg = ""
    msg = ""

    if request.method == "POST":
        if request.form.get("name") and request.form.get("address") and \
           request.form.get("gender_id") and request.form.get("city_id"):
            name = request.form.get("name")
            address = request.form.get("address")
            image = ""
            gender_id = request.form.get("gender_id")
            city_id = request.form.get("city_id")
            date_begin = league.date_begin
            date_end = request.form.get("date_end")
            user_id = current_user.id
            has_scheduled = False

            dao.update_league(league_id=league_id, name=name, address=address,
                              image=image, gender_id=int(gender_id),
                              city_id=int(city_id), date_begin=date_begin,
                              date_end=date_end, user_id=int(user_id), has_scheduled=has_scheduled)
            msg = "Cập nhật thông tin của giải đấu thành công !"

        else:
            err_msg = "Bạn phải nhập đầy đủ thông tin của giải đấu !"

    return render_template('settings.html', league=league, cities=cities, genders=genders,
                           msg=msg, err_msg=err_msg, date_now=date_now, check_date=check_date)


@app.route("/chi-tiet-tran-dau/<int:match_id>", methods=["get", "post"])
def match_detail(match_id):
    return render_template('match-detail.html')


# API
@app.route("/api/<int:league_id>/round/<string:round_name>")
def get_round_by_round_name(round_name, league_id):
    league = dao.read_league_by_id(league_id)
    round_name = int(round_name)
    matches = []

    for idx, round in enumerate(league.rounds):
        if round_name == idx + 1:
            for match in round.matches:
                m = {
                    'match_id': match.id,
                    'home': dao.read_club_name_by_club_id(match.home),
                    'home_id': match.home,
                    'home_score': dao.get_score_by_league_club_match(league_id=league_id,
                                                                     match_id=match.id, club_id=match.home),
                    'away': dao.read_club_name_by_club_id(match.away),
                    'away_id': match.away,
                    'away_score': dao.get_score_by_league_club_match(league_id=league_id,
                                                                     match_id=match.id, club_id=match.away),
                    'date': match.date,
                    'time': str(match.time)
                }
                matches.append(m)
            break
    return jsonify({'user_id': league.user_id, 'round': round_name, 'matches': matches})


@app.route("/api/update-date-match/<int:match_id>/<string:date>/<string:time>")
def update_date_match(match_id, date, time):
    dao.update_date_match(match_id=match_id, date=date, time=time)
    return jsonify({'status': 'success'})


@app.route("/api/match-detail/<int:match_id>")
def match_detail_by_match_id(match_id):
    url = url_for('match_detail', match_id=match_id)
    return jsonify({'url': url})


@app.route("/api/update-result-score-match/<int:league_id>/<int:match_id>/"
           "<int:home_id>/<int:home_score>/<int:away_id>/<int:away_score>")
def update_result_score_match(league_id, match_id, home_id, home_score, away_id, away_score):
    dao.update_result_score_match(league_id=league_id, match_id=match_id,
                                  home_id=home_id, home_score=home_score,
                                  away_id=away_id, away_score=away_score)
    return jsonify({'status': 'success'})


# TEMPLATE FILTER
@app.template_filter()
def get_total_player_by_club_id(club_id):
    return len(Club.query.get(club_id).players)


@app.template_filter()
def get_total_match_by_club_id(club_id):
    return len(Result.query.filter(Result.club_id == club_id).all())


@app.template_filter()
def get_club_name_by_club_id(club_id):
    return Club.query.get(club_id).name


@app.template_filter()
def get_club_phone_by_club_id(club_id):
    return Club.query.get(club_id).phone


@app.template_filter()
def get_status_name_by_status_id(status_id):
    return Status.query.get(status_id).name


@app.template_filter()
def get_status_color_by_status_id(status_id):
    return Status.query.get(status_id).color


@app.template_filter('get_total_match_by_club_id_in_league')
def get_total_match_by_club_id_in_league(club_id, league_id):
    return len(Result.query.filter(Result.league_id == league_id, Result.club_id == club_id).all())


@app.template_filter()
def get_total_club_of_league(league_id):
    return len(LeagueClub.query.filter(LeagueClub.league_id == league_id, LeagueClub.status_id == 2).all())


@app.template_filter('get_score_league_club_match')
def get_score_league_club_match(match_id, league_id, club_id):
    return Result.query.filter(Result.league_id == league_id,
                               Result.club_id == club_id,
                               Result.match_id == match_id).first().score


@app.template_filter()
def get_win_result_club(club_id):
    return len(Result.query.filter(Result.club_id == club_id, Result.type_result_id == 1).all())


@app.template_filter()
def get_draw_result_club(club_id):
    return len(Result.query.filter(Result.club_id == club_id, Result.type_result_id == 2).all())


@app.template_filter()
def get_lose_result_club(club_id):
    return len(Result.query.filter(Result.club_id == club_id, Result.type_result_id == 3).all())


if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)
