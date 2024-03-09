import wtforms
from wtforms.validators import length, email


class RegisterForm(wtforms.Form):
    usernum = wtforms.StringField(validators=[length(min=5, max=20)])
    userpwd = wtforms.StringField(validators=[length(min=6, max=100)])
    email = wtforms.StringField(validators=[email()])