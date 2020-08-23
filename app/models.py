from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from app import db, admin
from flask_admin import BaseView, expose
from flask_login import UserMixin


# Tạo bảng MySQL
class Club(db.Model):
    __tablename__ = "club"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    home = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    players = relationship('Player', backref='club', lazy=True)
    coaches = relationship('Coach', backref='club', lazy=True)
    results = relationship('Result', backref='club', lazy=True)

    def __str__(self):
        return self.name


class Coach(db.Model):
    __tablename__ = "coach"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birthday = Column(DateTime, nullable=False)
    description = Column(String(255), nullable=True)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)

    def __str__(self):
        return self.name


class TypePlayer(db.Model):
    __tablename__ = "type_player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    players = relationship('Player', backref='type_player', lazy=True)

    def __str__(self):
        return self.name


class Player(db.Model):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birthday = Column(DateTime, nullable=False)
    type_player_id = Column(Integer, ForeignKey(TypePlayer.id), nullable=False)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)
    goals = relationship('Goal', backref='player', lazy=True)

    def __str__(self):
        return self.name


class League(db.Model):
    __tablename__ = "league"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    rounds = relationship('Round', backref='league', lazy=True)

    def __str__(self):
        return self.name


class Round(db.Model):
    __tablename__ = "round"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    league_id = Column(Integer, ForeignKey(League.id), nullable=False)
    matches = relationship('Match', backref='round', lazy=True)

    def __str__(self):
        return self.name


class Match(db.Model):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, autoincrement=True)
    round_id = Column(Integer, ForeignKey(Round.id), nullable=False)
    home = Column(Integer, ForeignKey(Club.id), nullable=False)
    away = Column(Integer, ForeignKey(Club.id), nullable=False)
    stadium = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)

    def __str__(self):
        return self.id + " - " + self.home + " - " + self.away


class TypeGoal(db.Model):
    __tablename__ = "type_goal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class Goal(db.Model):
    __tablename__ = "goal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_goal_id = Column(Integer, ForeignKey(TypeGoal.id), nullable=False)
    player_id = Column(Integer, ForeignKey(Player.id), nullable=False)
    match_id = Column(Integer, ForeignKey(Match.id), nullable=False)

    def __str__(self):
        return self.id + " - " + self.player_id + " - " + self.match_id


class TypeResult(db.Model):
    __tablename__ = "type_result"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class Result(db.Model):
    __tablename__ = "result"

    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey(Match.id), nullable=False)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)
    type_result_id = Column(Integer, ForeignKey(TypeResult.id), nullable=False)

    def __str__(self):
        return self.id + " - " + self.match_id + " - " + self.club_id + " - " + self.type_result_id


class Rule(db.Model):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    number = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)

    def __str__(self):
        return self.name + " - " + self.number


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __str__(self):
        return self.name + " - " + self.username


class Administrator(db.Model, UserMixin):  # Đa kế thừa
    __tablename__ = "administrator"

    id = Column(Integer, primary_key=True, autoincrement=True)  # autoincrement: tăng tự động
    name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    def __str__(self):
        return self.name + " - " + self.username


# <<<<<<< HEAD

class ClubModelView(ModelView):
    column_display_pk = True
    create_modal = True
    can_view_details = True


class CoachModelView(ModelView):
    column_display_pk = True
    create_modal = True
    can_view_details = True
    list_template = 'create-league.html'


class TypePlayerModelView(ModelView):
    create_modal = True


class PlayerModelView(ModelView):
    create_modal = True


class LeagueModelView(ModelView):
    create_modal = True


class RoundModelView(ModelView):
    create_modal = True


class MatchModelView(ModelView):
    create_modal = True


class TypeGoalModelView(ModelView):
    create_modal = True


class GoalModelView(ModelView):
    create_modal = True


class TypeResultModelView(ModelView):
    create_modal = True


class ResultModelView(ModelView):
    create_modal = True


class RuleModelView(ModelView):
    create_modal = True


class UserModelView(ModelView):
    create_modal = True


class AdministratorModelView(ModelView):
    create_modal = True


# Tạo các trang admin
admin.add_view(ClubModelView(Club, db.session))
admin.add_view(CoachModelView(Coach, db.session))
admin.add_view(PlayerModelView(Player, db.session))
admin.add_view(LeagueModelView(League, db.session))
admin.add_view(RoundModelView(Round, db.session))
admin.add_view(MatchModelView(Match, db.session))
admin.add_view(GoalModelView(Goal, db.session))
admin.add_view(ResultModelView(Result, db.session))
admin.add_view(RuleModelView(Rule, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(AdministratorModelView(Administrator, db.session))
# admin.add_view(TypePlayer(TypePlayer, db.session))
# admin.add_view(TypeGoal(TypeGoal, db.session))
# admin.add_view(TypeResult(TypeResult, db.session))


class HomeAdmin(BaseView):
    @expose('/')
    def index (self):
        return self.render('admin/About us.html')


admin.add_view(HomeAdmin(name="About Us"))


if __name__ == "__main__":
    db.create_all()
