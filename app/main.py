from app.models import *
from app import app, dao, login
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required


@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@login.user_loader
def admin_loader(admin_id):
    return Administrator.query.get(admin_id)


# ADMIN
@app.route("/admin/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # user = dao.check_login(username=username, password=password)
        administrator = dao.login_admin(username=username, password=password)

        # if user:
        #     login_user(user=user)
        if administrator:
            login_user(user=administrator)
            return redirect("/admin")
        else:
            err_msg = "Tên tài khoản hoặc mật khẩu không hợp lệ."
            return err_msg


# USER
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/giai-dau")
def league():
    cities = dao.read_city()
    type_competition = dao.read_type_competition()
    return render_template("leagues.html", cities=cities, type_competition=type_competition)


@app.route("/doi")
def club():
    levels = dao.read_level()
    genders = dao.read_gender()
    return render_template("clubs.html", levels=levels, genders=genders)


@app.route("/dang-nhap", methods=["get", "post"])
def login():
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
            return err_msg

    return render_template("login.html", err_msg=err_msg)


@app.route("/dang-ky", methods=["get", "post"])
def register():
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


@app.route("/thong-tin-ca-nhan")
@login_required
def profile():
    return render_template('profile.html')


@app.route("/quan-ly-giai-dau")
@login_required
def my_league():
    return render_template('my-league.html')


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


@app.route("/tao-giai-dau")
@login_required
def create_league():
    genders = dao.read_gender()
    cities = dao.read_city()
    type_competition = dao.read_type_competition()
    return render_template("create-league.html", genders=genders, cities=cities, type_competition=type_competition)


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


@app.route("/chi-tiet-giai-dau")
def league_detail():
    return render_template('league-detail.html')


@app.route("/xep-hang")
def rank():
    return render_template('rank.html')


@app.route("/cac-doi-cua-giai-dau")
def clubs_league():
    return render_template('clubs-league.html')


@app.route("/thong-ke")
def statistic():
    return render_template('statistic.html')


if __name__ == "__main__":
    from app import admin
    app.run(debug=True)
