from app import app, dao, login
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime


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

    keyword = request.args["keyword"] if request.args.get("keyword") else ""
    city_id = request.args["city_id"] if request.args.get("city_id") else 0
    leagues = dao.read_league(keyword=keyword, city_id=city_id)

    return render_template("leagues.html", cities=cities, leagues=leagues,
                           keyword=keyword, city_id=city_id)


@app.route("/doi")
def club():
    levels = dao.read_level()
    genders = dao.read_gender()
    return render_template("clubs.html", levels=levels, genders=genders)


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
    convert_birthday = user.birthday.strftime("%Y-%m-%d")
    err_msg = ""

    if request.method == "POST":
        if request.form.get("name") and request.form.get("phone") and request.form.get("birthday"):
            name = request.form.get("name")
            phone = request.form.get("phone")
            birthday = request.form.get("birthday")

            dao.update_profile(user_id=user_id, name=name, phone=phone, birthday=birthday)
            msg = "Cập nhật thành công !"

            return render_template('profile.html', user=user, msg=msg, convert_birthday=convert_birthday)
        else:
            err_msg = "Bạn phải nhập đủ thông tin !"

    return render_template('profile.html', user=user, err_msg=err_msg, convert_birthday=convert_birthday)


@app.route("/quan-ly-giai-dau")
@login_required
def my_league():
    leagues = dao.read_leagues_by_user_id(current_user.id)
    return render_template('my-league.html', leagues=leagues)


@app.route("/quan-ly-doi-bong")
@login_required
def my_club():
    return render_template('my-club.html')


@app.route("/tao-doi")
@login_required
def create_club():
    levels = dao.read_level()
    genders = dao.read_gender()
    return render_template("create-club.html", levels=levels, genders=genders)


@app.route("/tao-giai-dau", methods=["get", "post"])
@login_required
def create_league():
    genders = dao.read_gender()
    cities = dao.read_city()

    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        image = ''
        gender_id = request.form.get("gender_id")
        city_id = request.form.get("city_id")
        user_id = current_user.id

        dao.create_league(name=name, address=address, image=image,
                          gender_id=gender_id, city_id=city_id, user_id=user_id)

    return render_template("create-league.html", genders=genders, cities=cities)


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


@app.route("/chi-tiet-giai-dau/<int:league_id>")
def league_detail(league_id):
    cities = dao.read_city()
    league = dao.read_league_by_id(league_id)
    return render_template('league-detail.html', league=league, cities=cities)


@app.route("/xep-hang/<int:league_id>")
def rank(league_id):
    cities = dao.read_city()
    league = dao.read_league_by_id(league_id)
    return render_template('rank.html', league=league, cities=cities)


@app.route("/cac-doi-cua-giai-dau/<int:league_id>")
def clubs_league(league_id):
    cities = dao.read_city()
    league = dao.read_league_by_id(league_id)
    return render_template('clubs-league.html', league=league, cities=cities)


@app.route("/thong-ke/<int:league_id>")
def statistic(league_id):
    cities = dao.read_city()
    league = dao.read_league_by_id(league_id)
    return render_template('statistic.html', league=league, cities=cities)


if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)
