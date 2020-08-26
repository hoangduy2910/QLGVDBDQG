from app import db, admin
from flask_admin.contrib.sqla import ModelView
from app.models import *


# Tạo các trang admin
# admin.add_view(ModelView(TypePlayer, db.session))
# admin.add_view(ModelView(TypeGoal, db.session))
# admin.add_view(ModelView(TypeResult, db.session))
# admin.add_view(ModelView(TypeCompetition, db.session))
admin.add_view(ModelView(Club, db.session))
admin.add_view(ModelView(Player, db.session))
admin.add_view(ModelView(League, db.session))
admin.add_view(ModelView(Round, db.session))
admin.add_view(ModelView(Match, db.session))
admin.add_view(ModelView(Goal, db.session))
admin.add_view(ModelView(Result, db.session))
admin.add_view(ModelView(Rule, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Administrator, db.session))