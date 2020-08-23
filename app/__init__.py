from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = "b\xf5!\x82x\xcd\xa6$d\\<\xf0.\x05j\x0b\x80"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/db_qlgiaibongda?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

# Đối tượng xử lý Admin
admin = Admin(app=app, name="Quản Lý Giải Vô Địch Bóng Đá Quốc Gia", template_mode="bootstrap3")

# Đối tượng xử lý Login
login = LoginManager(app=app)

