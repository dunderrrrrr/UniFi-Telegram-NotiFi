import os
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class TelegramMessage(FlaskForm):
    tgmsg = TextAreaField('Telegram Message', validators=[DataRequired()])
