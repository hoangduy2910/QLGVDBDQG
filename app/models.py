from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# Tạo bảng MySQL
class TypeCompetition(db.Model):
    __tablename__ = "type_competition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class TypeResult(db.Model):
    __tablename__ = "type_result"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class TypeGoal(db.Model):
    __tablename__ = "type_goal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class TypePlayer(db.Model):
    __tablename__ = "type_player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    players = relationship('Player', backref='type_player', lazy=True)

    def __str__(self):
        return self.name


class Club(db.Model):
    __tablename__ = "club"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    home = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    players = relationship('Player', backref='club', lazy=True)
    results = relationship('Result', backref='club', lazy=True)

    def __str__(self):
        return self.name


class Player(db.Model):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birthday = Column(DateTime, nullable=False)
    image = Column(String(255), nullable=True)
    type_player_id = Column(Integer, ForeignKey(TypePlayer.id), nullable=False)
    club_id = Column(Integer, ForeignKey(Club.id), nullable=False)
    goals = relationship('Goal', backref='player', lazy=True)

    def __str__(self):
        return self.name


class League(db.Model):
    __tablename__ = "league"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type_competition_id = Column(Integer, ForeignKey('type_competition.id'), nullable=False)
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


class Goal(db.Model):
    __tablename__ = "goal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_goal_id = Column(Integer, ForeignKey(TypeGoal.id), nullable=False)
    player_id = Column(Integer, ForeignKey(Player.id), nullable=False)
    match_id = Column(Integer, ForeignKey(Match.id), nullable=False)

    def __str__(self):
        return self.id + " - " + self.player_id + " - " + self.match_id


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
        return self.username


class Administrator(db.Model):
    __tablename__ = "administrator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __str__(self):
        return self.name + " - " + self.username


if __name__ == "__main__":
    db.create_all()
