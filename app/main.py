from flask import render_template, redirect, request
from app import app
from app.models import *
from app import login
from flask_login import login_user
# thư viện để băm mật khẩu
import hashlib


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
    return render_template("create-league.html")


@app.route("/tim-giai-dau")
def find_league():
    return render_template("find-league.html")


@app.route("/tim-doi")
def find_team():
    return render_template("find-team.html")


@app.route("/dang-nhap")
def login():
    return render_template("admin-login.html")


@app.route("/dang-ky")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
