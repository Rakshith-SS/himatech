from flask import flash, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from himatech.models import User, Items
from flask_login import current_user
import re

namePattern = '^[a-zA-Z]\w+$'
emailPattern = "^[a-zA-Z0-9_.]+[@][a-z]+(\.[a-z]+)?\.(com|net|edu|in|ch|org|info|fr|eu|io|de)" 

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,max=32)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(), Length(min=3,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])    
    password = PasswordField('Password', 
                            [DataRequired(),
                            Length(min=6,max=32),
                            validators.EqualTo('confirm_password',
                            message='Passwords must match')])
    
    confirm_password = PasswordField(label="Repeat Password")
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(f'{username.data} is already taken')

        if re.search(namePattern, username.data):
            pass
        else:
            raise ValidationError(f'{username.data} is not valid username')

        if re.search('^\d', username.data):
            raise ValidationError(f'Username cannot begin with a number')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(f'{email.data} is already taken')

        if re.search(emailPattern, email.data):
            pass
        else:
            raise ValidationError(f'{email.data} is an invalid email')

class UpdateAccountInfo(FlaskForm):   
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Account')

    def validate_username(self,username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(f'{username.data} is already taken')

    def validate_email(self,email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError(f'{email.data} is already taken')

class AddToCart(FlaskForm):
    submit = SubmitField('Add To Cart')

class RemoveCartItem(FlaskForm):
    submit = SubmitField('Remove Item')

class CheckOut(FlaskForm):
    city = SelectField('Select City', choices= ['Indiranagar', 'Kormangala', 'Jaynagar', 'Sarjapur'] )
    street = IntegerField('Street Number', validators = [DataRequired(), Length(min=1, max=3)])
    doorNumber = IntegerField('Door Number', validators=[DataRequired(), Length(min=1, max=2)])
    submit = SubmitField('CheckOut')
