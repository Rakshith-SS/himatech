from datetime import datetime
from phonenumbers import phonenumber
from himatech import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader                          #loads the user from the database
def load_user(id):
    return User.query.get(int(id))

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(120))
    product_name = db.Column(db.String(100))
    product_quantity = db.Column(db.Integer)
    product_image = db.Column(db.String(100))
    product_price = db.Column(db.Integer)
    checkout  = db.Column(db.Boolean, default=False)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(30))
    address = db.Column(db.String(300))
    phoneNumber = db.Column(db.Integer)
    company = db.Column(db.String(150))
    country = db.Column(db.String(100), default="India")
    city = db.Column(db.String(100))
    pincode = db.Column(db.String(6))
    state = db.Column(db.String(30), default="Karnataka")
    checkoutTime = db.Column(db.DateTime, default=datetime.utcnow)
    invoiceNumber = db.Column(db.String(16))
    def __repr__(self):
        return f'Cart ({self.username}, {self.product_name}, {self.product_price})'

class Items(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50))
    product_name = db.Column(db.String(100))
    product_desc = db.Column(db.Text)
    product_price = db.Column(db.Integer)
    product_images = db.Column(db.JSON)
    product_quantity_left = db.Column(db.Integer)
    product_sold_totally = db.Column(db.Integer)
    category = db.Column(db.String(100))
    year_of_manufacture = db.Column(db.Integer)
    warranty = db.Column(db.Integer)
    model_number = db.Column(db.String(100))
    discount_percent = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    specifications = db.Column(db.JSON)

    def __repr__(self):
        return f'Items <Product Name -{self.product_name} , Product Price - {self.product_price}, Category - {self.category}>'

class Wishlist(db.Model):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    wishlist_item = db.Column(db.String(100))
    wishlist_image = db.Column(db.String(100))
    wishlist_item_price = db.Column(db.Integer)
    username = db.Column(db.String(32))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f'Wishlist ({self.username}, {self.wishlist_item})'

class User(UserMixin ,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(128), nullable=False, default="default.jpg")
    phonenumber = db.Column(db.String(13))
    password_hash = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean, default=False)
    verification_email_sent_on = db.Column(db.DateTime)
    email_confirmed_on = db.Column(db.DateTime)


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
