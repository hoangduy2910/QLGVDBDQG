from app import admin, db
from app.models import *
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class ClubModelView(AuthenticatedView):
    column_display_pk = True
    create_modal = True
    can_view_details = True


class CoachModelView(AuthenticatedView):
    column_display_pk = True
    create_modal = True
    can_view_details = True
    list_template = 'create-league.html'


class TypePlayerModelView(AuthenticatedView):
    create_modal = True


class PlayerModelView(AuthenticatedView):
    create_modal = True


class LeagueModelView(AuthenticatedView):
    create_modal = True


class RoundModelView(AuthenticatedView):
    create_modal = True


class MatchModelView(AuthenticatedView):
    create_modal = True


class TypeGoalModelView(AuthenticatedView):
    create_modal = True


class GoalModelView(AuthenticatedView):
    create_modal = True


class TypeResultModelView(AuthenticatedView):
    create_modal = True


class ResultModelView(AuthenticatedView):
    create_modal = True


class RuleModelView(AuthenticatedView):
    create_modal = True


class UserModelView(AuthenticatedView):
    create_modal = True


class AdministratorModelView(AuthenticatedView):
    create_modal = True


# Log out
class LogOutView(BaseView):
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
admin.add_view(LogOutView(name="Logout"))

