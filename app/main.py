from app import app
from flask import render_template
from app.models import *


@app.route("/")
def index():
    return render_template("index.html")


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
    return render_template("login.html")


@app.route("/dang-ky")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)