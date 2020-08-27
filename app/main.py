from flask import render_template, redirect, request
from app import app
from app.models import *
from app import login
from flask_login import login_user
# thư viện để băm mật khẩu
import hashlib

from app import dao
from flask import render_template, request, redirect, url_for, session, jsonify



@app.route("/")
def index():
    return render_template("index.html")


@login.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = Administrator.query.filter(Administrator.username == username.strip(),
                                          Administrator.password == password).first()
        # .first() => nếu có thì trả ra ngược lại trả ra null
        # .strip() => cắt 2 đầu khoảng trắng

        if user:
            login_user(user=user)
    return redirect("/admin")


@app.route("/tao-giai-dau")
def create_league():
    return render_template("create-leagues.html")


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
    return render_template("admin-login.html")
    err_msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = dao.check_login(username=username, password=password)

        if user:
            user_json = {
                'id': user.id,
                'name': user.name,
                'username': user.username
            }
            session["user"] = user_json
            return redirect(url_for('index'))
        else:
            err_msg = "Tên tài khoản hoặc mật khẩu không hợp lệ."

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
def logout():
    if "user" in session:
        session["user"] = None
    return redirect(url_for('index'))


@app.route("/thong-tin-ca-nhan")
def profile():
    return render_template('profile.html')


@app.route("/quan-ly-giai-dau")
def my_league():
    return render_template('my-league.html')


@app.route("/quan-ly-doi-bong")
def my_club():
    return render_template('my-club.html')


if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True)
=======
    from app.admin import *
    app.run(debug=True)
>>>>>>> aba7ebebd635910c5480ca2b17a5110152c36ed4
