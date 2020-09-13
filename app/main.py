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
    msg = ""

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        birthday = request.form.get("birthday")

        dao.update_profile(user_id=user_id, name=name, phone=phone, birthday=birthday)
        msg = "Cập nhật thành công !"

    return render_template('profile.html', user=user, msg=msg)


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

        club = dao.create_club(name=name, phone=phone, address=address, image=image,
                               gender_id=int(gender_id), level_id=int(level_id), user_id=user_id)

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        return redirect(url_for('club_detail', club_id=club.id))

    return render_template("create-club.html", levels=levels, genders=genders)


@app.route("/tao-giai-dau", methods=["get", "post"])
@login_required
def create_league():
    genders = dao.read_gender()
    cities = dao.read_city()
    date_now = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    msg = ""

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
        win_point = request.form.get("win_point")
        draw_point = request.form.get("draw_point")
        lose_point = request.form.get("lose_point")

        if dao.check_point_win_draw_lose(win_point=int(win_point), draw_point=int(draw_point),
                                         lose_point=int(lose_point)):
            league = dao.create_league(name=name, address=address, image=image, gender_id=int(gender_id),
                                       city_id=int(city_id), date_begin=date_begin, date_end=date_end,
                                       user_id=int(user_id), has_scheduled=has_scheduled, win_point=int(win_point),
                                       draw_point=int(draw_point), lose_point=int(lose_point))

            return redirect(url_for('create_rule', league_id=league.id))
        else:
            msg = "Điểm thắng phải lớn hơn điểm hòa và điểm hòa phải lớn hơn điểm thua !!!"

    return render_template("create-league.html", genders=genders, cities=cities, date_now=date_now, msg=msg)


@app.route("/them-cau-thu/<int:club_id>", methods=["get", "post"])
@login_required
def create_player(club_id):
    type_player = dao.read_type_player()

    if request.method == "POST":
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        image = ""
        type_player_id = request.form.get("type_player_id")
        club_id = club_id

        dao.create_player(name=name, birthday=birthday, phone=phone, image=image,
                          type_player_id=type_player_id, club_id=club_id)

        return redirect(url_for('players_club', club_id=club_id))

    return render_template('create-player.html', type_player=type_player)


@app.route("/tao-quy-dinh-giai-dau/<int:league_id>", methods=["get", "post"])
@login_required
def create_rule(league_id):
    league = dao.read_league_by_id(league_id)
    if request.method == "POST":
        min_age = request.form.get("min_age")
        max_age = request.form.get("max_age")
        min_player = request.form.get("min_player")
        max_player = request.form.get("max_player")
        max_foreign_player = request.form.get("max_foreign_player")

        rule = dao.create_rule(min_age=int(min_age), max_age=int(max_age), min_player=int(min_player),
                               max_player=int(max_player), max_foreign_player=int(max_foreign_player),
                               league_id=int(league_id))

        return render_template('register-league.html', league_id=league_id, league=league, rule=rule)

    return render_template('create-rule.html', league_id=league_id)


@app.route("/chi-tiet-doi-bong/<int:club_id>", methods=["get", "post"])
def club_detail(club_id):
    cities = dao.read_city()
    genders = dao.read_gender()
    levels = dao.read_level()
    club = dao.read_club_by_club_id(club_id)
    msg = ""

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        image = ""
        gender_id = request.form.get("gender_id")
        level_id = request.form.get("level_id")
        user_id = current_user.id

        dao.update_club(club_id=club_id, name=name, phone=phone, address=address, image=image,
                        gender_id=int(gender_id), level_id=int(level_id), user_id=int(user_id))
        msg = "Cập nhật thông tin của đội bóng thành công !"

    return render_template('club-detail.html', levels=levels, cities=cities, genders=genders, club=club, msg=msg)


@app.route("/cau-thu-cua-doi/<int:club_id>")
def players_club(club_id):
    club = dao.read_club_by_club_id(club_id)
    return render_template('players-club.html', club=club)


@app.route("/giai-dau-cua-doi/<int:club_id>")
def leagues_club(club_id):
    club = dao.read_club_by_club_id(club_id=club_id)
    league_club = dao.read_club_in_league_club(club_id=club_id)
    return render_template('leagues-club.html', league_club=league_club, club=club)


@app.route("/thanh-tich-cua-doi/<int:club_id>")
def achievements(club_id):
    club = dao.read_club_by_club_id(club_id)
    return render_template('achievements.html', club=club)


@app.route("/chi-tiet-cau-thu/<int:player_id>", methods=["get", "post"])
def player_detail(player_id):
    player = dao.read_player_by_player_id(player_id)
    type_player = dao.read_type_player()
    user = dao.get_user_by_club_id(player.club_id)
    msg = ""

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        birthday = request.form.get("birthday")
        image = ""
        type_player_id = request.form.get("type_player_id")
        club_id = player.club_id

        dao.update_player(player_id=player.id, name=name, phone=phone, birthday=birthday,
                          image=image, type_player_id=type_player_id, club_id=club_id)

        msg = "Cập nhật cầu thủ thành công !!!"

    return render_template('player-detail.html', player=player, user=user, type_player=type_player, msg=msg)


@app.route("/dang-ky-thi-dau/<int:league_id>", methods=["get", "post"])
def register_league(league_id):
    rule = dao.get_rules_by_league_id(league_id)
    cities = dao.read_city()
    msg = ""

    if request.method == "POST":
        league_id = league_id
        club_id = request.form.get("club_id")
        status_id = 1

        total_player = dao.get_total_player_by_club_id(int(club_id))
        if rule.min_player <= total_player <= rule.max_player:
            dao.create_league_club(league_id=league_id, club_id=int(club_id), status_id=status_id)
            msg = {
                "alert_type": "success",
                "content": "Đăng ký đội bóng thành công !!!"
            }
        else:
            msg = {
                "alert_type": "warning",
                "content": "Số lượng cầu thủ tối thiểu của đội là "
                           + str(rule.min_player) + " và tối đa là " + str(rule.max_player)
            }

    league = dao.read_league_by_id(league_id)
    league_club = dao.get_club_id_in_league_club_by_league_id(league_id)

    check_date = False
    date_now = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_end = (league.date_end + timedelta(days=1)).strftime('%Y-%m-%d')

    if date_now <= date_end:
        check_date = True

    return render_template('register-league.html', league=league, rule=rule, cities=cities, date_now=date_now,
                           date_end=date_end, check_date=check_date, league_club=league_club, msg=msg)


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
                              date_end=(date_now - timedelta(days=1)), user_id=league.user_id,
                              has_scheduled=True, win_point=league.win_point,
                              draw_point=league.draw_point, lose_point=league.lose_point)

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

    league_club = dao.read_league_club_by_rank(league_id=league_id)

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
            date_end = league.date_end
            user_id = current_user.id
            has_scheduled = True
            win_point = request.form.get("win_point")
            draw_point = request.form.get("draw_point")
            lose_point = request.form.get("lose_point")

            if dao.check_point_win_draw_lose(win_point=int(win_point), draw_point=int(draw_point),
                                             lose_point=int(lose_point)):
                dao.update_league(league_id=league_id, name=name, address=address, image=image,
                                  gender_id=int(gender_id), city_id=int(city_id), date_begin=date_begin,
                                  date_end=date_end, user_id=int(user_id), has_scheduled=has_scheduled,
                                  win_point=int(win_point), draw_point=int(draw_point), lose_point=int(lose_point))

            msg = "Cập nhật thông tin của giải đấu thành công !"

    return render_template('settings.html', league=league, cities=cities, genders=genders,
                           msg=msg, err_msg=err_msg, date_now=date_now, check_date=check_date)


@app.route("/quy-dinh-giai-dau/<int:league_id>", methods=["get", "post"])
def rules(league_id):
    league = dao.read_league_by_id(league_id)
    rules = dao.get_rules_by_league_id(league_id)
    cities = dao.read_city()
    check_date = dao.check_date_end_league(league.date_end)
    msg = ""

    if request.method == "POST":
        min_age = request.form.get("min_age")
        max_age = request.form.get("max_age")
        min_player = request.form.get("min_player")
        max_player = request.form.get("max_player")
        max_foreign_player = request.form.get("max_foreign_player")

        dao.update_rule(min_age=int(min_age), max_age=int(max_age), min_player=int(min_player),
                        max_player=int(max_player), max_foreign_player=int(max_foreign_player),
                        league_id=int(league_id))

        msg = "Cập nhật quy định giải đấu thành công !!!"

    return render_template('rules.html', league=league, rules=rules, cities=cities, check_date=check_date, msg=msg)


@app.route("/chi-tiet-tran-dau/<int:match_id>", methods=["get", "post"])
def match_detail(match_id):
    match = dao.read_match_by_match_id(match_id)
    user = dao.get_user_by_league_id(league_id=match.league_id)
    type_goal = dao.read_type_goal()
    goals = dao.get_goals_by_match_id(match_id=match_id)

    if request.method == "POST":
        club_id = request.form.get("club_id")
        player_id = request.form.get("player_id")
        time = request.form.get("time")
        type_goal_id = request.form.get("type_goal_id")
        match_id = match_id

        dao.create_goal(time=time, type_goal_id=int(type_goal_id), player_id=int(player_id),
                        club_id=int(club_id), match_id=int(match_id))

        if int(type_goal_id) == 2:
            dao.update_score_league_club(league_id=match.league_id, match_id=match_id, club_id=match.away)
        else:
            dao.update_score_league_club(league_id=match.league_id, match_id=match_id, club_id=club_id)

        return redirect(url_for('match_detail', match_id=match_id))

    return render_template('match-detail.html', match=match, user=user, type_goal=type_goal, goals=goals)


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
                    'time': str(match.time),
                    'is_ended': match.is_ended
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


@app.route("/api/detele-player/<int:player_id>")
def player_detail_by_player_id(player_id):
    dao.delete_player(player_id=player_id)
    return jsonify({'status': 'success'})


@app.route("/api/get-players-of-club/<int:club_id>")
def get_players_of_club(club_id):
    club = dao.read_club_by_club_id(club_id=club_id)
    players = club.players
    players_json = []
    for player in players:
        p = {
            'player_id': player.id,
            'name': player.name
        }
        players_json.append(p)

    return jsonify({'players': players_json})


@app.route("/api/end-match/<int:match_id>")
def end_match_league_club(match_id):
    dao.end_match_league_club(match_id)
    url = url_for('match_detail', match_id=match_id)
    return jsonify({'url': url})


# TEMPLATE FILTER
@app.template_filter()
def get_total_player_by_club_id(club_id):
    return dao.get_total_player_by_club_id(club_id)


@app.template_filter()
def get_total_match_by_club_id(club_id):
    return dao.get_total_match_by_club_id(club_id)


@app.template_filter('get_total_match_by_club_id_in_league')
def get_total_match_by_club_id_in_league(club_id, league_id):
    return dao.get_total_match_by_club_id_in_league(club_id, league_id)


@app.template_filter()
def get_total_club_of_league(league_id):
    return dao.get_total_club_of_league(league_id)


@app.template_filter()
def get_club_name_by_club_id(club_id):
    return dao.get_club_name_by_club_id(club_id)


@app.template_filter()
def get_club_phone_by_club_id(club_id):
    return dao.get_club_phone_by_club_id(club_id)


@app.template_filter()
def get_status_name_by_status_id(status_id):
    return dao.get_status_name_by_status_id(status_id)


@app.template_filter()
def get_status_color_by_status_id(status_id):
    return dao.get_status_color_by_status_id(status_id)


@app.template_filter('get_score_league_club_match')
def get_score_league_club_match(match_id, league_id, club_id):
    return dao.get_score_league_club_match(match_id, league_id, club_id)


@app.template_filter()
def get_win_result_club(club_id):
    return dao.get_win_result_club(club_id)


@app.template_filter()
def get_draw_result_club(club_id):
    return dao.get_draw_result_club(club_id)


@app.template_filter()
def get_lose_result_club(club_id):
    return dao.get_lose_result_club(club_id)


@app.template_filter('get_win_result_league_club')
def get_win_result_league_club(club_id, league_id):
    return dao.get_win_result_league_club(club_id, league_id)


@app.template_filter('get_draw_result_league_club')
def get_draw_result_league_club(club_id, league_id):
    return dao.get_draw_result_league_club(club_id, league_id)


@app.template_filter('get_lose_result_league_club')
def get_lose_result_league_club(club_id, league_id):
    return dao.get_lose_result_league_club(club_id, league_id)


@app.template_filter()
def get_level_name_by_level_id(level_id):
    return dao.get_level_name_by_level_id(level_id)


@app.template_filter()
def get_gender_name_by_gender_id(gender_id):
    return dao.get_gender_name_by_gender_id(gender_id)


@app.template_filter()
def get_league_name_by_league_id(league_id):
    return dao.get_league_name_by_league_id(league_id)


@app.template_filter()
def get_type_player_name_by_type_player_id(type_player_id):
    return dao.get_type_player_name_by_type_player_id(type_player_id)


@app.template_filter()
def get_total_goal_by_player_id(player_id):
    return dao.get_total_goal_by_player_id(player_id)


@app.template_filter('get_goal_difference_league_club')
def get_goal_difference_league_club(club_id, league_id):
    return dao.get_goal_difference_by_league_club(league_id=league_id, club_id=club_id)


@app.template_filter('get_point_league_club')
def get_point_league_club(club_id, league_id):
    return dao.get_point_league_club(league_id=league_id, club_id=club_id)


@app.template_filter()
def get_player_name_by_player_id(player_id):
    return dao.get_player_name_by_player_id(player_id)


@app.template_filter()
def get_type_goal_name_by_type_goal_id(type_goal_id):
    return dao.get_type_goal_name_by_type_goal_id(type_goal_id)


@app.template_filter()
def get_normal_goals_by_club_id(club_id):
    return dao.get_normal_goals_by_club_id(club_id)


@app.template_filter()
def get_own_goals_by_club_id(club_id):
    return dao.get_own_goals_by_club_id(club_id)


@app.template_filter()
def get_free_kick_goals_by_club_id(club_id):
    return dao.get_free_kick_goals_by_club_id(club_id)


@app.template_filter()
def get_penalty_goals_by_club_id(club_id):
    return dao.get_penalty_goals_by_club_id(club_id)


if __name__ == "__main__":
    from app.admin import *

    app.run(debug=True)
