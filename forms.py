from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo 

class LoginForm(FlaskForm):
    csrf_token = StringField()
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired(), EqualTo("confirm_password")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    confirm_email = StringField("Confirm Email", validators=[DataRequired()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    submit = SubmitField('Login')
    
    