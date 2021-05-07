import os
from datetime import datetime
from himatech import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



@login.user_loader                          #loads the user from the database
def load_user(id):
    return User.query.get(int(id))

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(120))
    product_name = db.Column(db.String(32))
    product_quantity = db.Column(db.Integer)
    product_image = db.Column(db.String(100))
    product_price = db.Column(db.Integer)
    checkout  = db.Column(db.String(4), default="False")

    def __repr__(self):
        return f'Cart ({self.username}, {self.product_name}, {self.product_price})'

class Items(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(32), unique=True)
    product_desc = db.Column(db.String(500))
    product_price = db.Column(db.Integer)
    product_image = db.Column(db.String(100))
    product_quantity_left = db.Column(db.Integer)

    def __repr__(self):
        return f'Items ({self.product_name} , {self.product_price}, {self.product_quantity_left})'


class User(UserMixin ,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(128), nullable=False, default="default.jpg")
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def password(self):
        raise AttributeError('Password is not a readable attribute')


    def __repr__(self):
        return f'User ({self.username})'

    def get_id(self):
        return self.user_id

