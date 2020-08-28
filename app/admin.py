from app import admin, db
from app.models import *
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class PlayerModelView(AuthenticatedView):
    create_modal = True


class ClubModelView(AuthenticatedView):
    create_modal = True


class MatchModelView(AuthenticatedView):
    create_modal = True


class RoundModelView(AuthenticatedView):
    create_modal = True


class LeagueModelView(AuthenticatedView):
    create_modal = True


class GoalModelView(AuthenticatedView):
    create_modal = True


class ResultModelView(AuthenticatedView):
    create_modal = True


class RuleModelView(AuthenticatedView):
    create_modal = True


class UserModelView(AuthenticatedView):
    create_modal = True


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(PlayerModelView(Player, db.session))
admin.add_view(ClubModelView(Club, db.session))
admin.add_view(MatchModelView(Match, db.session))
admin.add_view(RoundModelView(Round, db.session))
admin.add_view(LeagueModelView(League, db.session))
admin.add_view(GoalModelView(Goal, db.session))
admin.add_view(ResultModelView(Result, db.session))
admin.add_view(RuleModelView(Rule, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(LogoutView(name="Logout"))

