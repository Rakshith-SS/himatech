from flask import flash, redirect,url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from phonenumbers import phonenumber
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from himatech.models import User, Items, Wishlist
from flask_login import current_user
import re
import phonenumbers


namePattern = '^[a-zA-Z]\w+$'
emailPattern = "^[a-zA-Z0-9_.]+[@][a-z]+(\.[a-z]+)?\.(com|net|edu|in|ch|org|info|fr|eu|io|de)$" 
numberPattern = r"^(\+91|0|)[0-9]{10}$"
phone = re.compile(numberPattern)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,max=64)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(), Length(min=3,max=32)])
    email = StringField('Email', validators=[DataRequired(), Email()])    
    password = PasswordField('Password', 
                            [DataRequired(),
                            Length(min=6,max=64),
                            validators.EqualTo('confirm_password',
                            message='Passwords must match')])
    mobileNumber = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=13)])
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
        
    def validate_mobileNumber(self,mobileNumber):
        numberExist = User.query.filter_by(phonenumber= mobileNumber.data).first() 
        if numberExist is not None: 
            raise ValidationError(f'{mobileNumber.data} is already taken') 
        if phone.match(mobileNumber.data): 
            mobile = phonenumbers.parse(mobileNumber.data, "IN") 
            checkNumber = phonenumbers.is_valid_number(mobile) 
            if checkNumber:
                pass  #valid mobile Number 
            else: 
                raise ValidationError("Enter a valid phone Number") 
        else: 
            raise ValidationError("Phone Numbers must start 0, +91 or the 10 digit number itself")


class ChangeProfilePicture(FlaskForm):
    picture = FileField('Change Photo', validators=[FileAllowed(['jpg','png', 'jpeg'])])

    def validate_picture(self, picture):
        pass
    

class UpdateAccountInfo(FlaskForm):   
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6,max=64)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                    DataRequired(), 
                                    Length(min=6, max=64), 
                                    validators.EqualTo('new_password',
                                    message='Passwords must match'
                                    )])
    submit = SubmitField('Save Changes')

    def validate_username(self,username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(f'{username.data} is already taken')        
        if re.search(namePattern, username.data):
            pass
        else:
            raise ValidationError(f'{username.data} is not valid username')
        if re.search('^\d', username.data):
            raise ValidationError(f'Username cannot begin with a number')

    def validate_email(self,email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError(f'{email.data} is already taken')
        
        if re.search(emailPattern, email.data):
            pass
        else:
            raise ValidationError(f'{email.data} is an invalid email')

    def validate_current_password(self, current_password):
        user = User.query.filter_by(username=current_user.username).first()
        if user.check_password(current_password.data):
            pass
        else:
            raise ValidationError("Incorrect password, try again!")


class AddToWishlist(FlaskForm):
    submit = SubmitField('Add To Wishlist')
    

class AddToCart(FlaskForm):
    submit = SubmitField('Add To Cart')

class RemoveCartItem(FlaskForm):
    submit = SubmitField('Remove Item')

class GoToCheckout(FlaskForm):
    submit = SubmitField('Checkout')

class CheckOut(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=3, max=32)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=32)])
    address = StringField('ADDRESS', validators=[DataRequired(), Length(min=10, max=300)])
    mobileNumber = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=13)])
    company = StringField('Company/Organisation Detail(Optional)')
    pincode = SelectField('Pincode',choices=["560008", "560025", "560026"] , validate_choice=True)
    city = SelectField('City',choices=["Indirangar", "Richmond", "Shantinagar"], validate_choice=True)
    submit = SubmitField('Confirm')


    def validate_mobileNumber(self,mobileNumber):
        if phone.match(mobileNumber.data):
            mobile = phonenumbers.parse(mobileNumber.data, "IN")
            checkNumber = phonenumbers.is_valid_number(mobile)
            if checkNumber:
                pass  #valid mobile Number
            else:
                raise ValidationError("Enter a valid phone Number")
        else:
            raise ValidationError("Phone Numbers must start 0, +91 or the 10 digit number itself")

class CancelOrder(FlaskForm):
    cancelOrder = SubmitField('Cancel Order')


class WishlistAddToCart(FlaskForm):
    submit = SubmitField('Add to Cart')

class RemoveFromWishlist(FlaskForm):
    submit = SubmitField('Remove')

class ClearWishlist(FlaskForm):
    submit = SubmitField('Clear Wishlist')
