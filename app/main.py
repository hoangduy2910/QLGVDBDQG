from app import app
from flask import render_template


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


@app.route("/dang-ky")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    from app.admin import *
    app.run(debug=True)