from app import app
from app import dao
from flask import render_template, request, redirect, url_for


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tao-giai-dau")
def create_league():
    return render_template("create-league.html")


@app.route("/giai-dau")
def league():
    return render_template("league.html")


@app.route("/doi")
def team():
    return render_template("team.html")


@app.route("/dang-nhap")
def login():
    return render_template("login.html")


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


if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)