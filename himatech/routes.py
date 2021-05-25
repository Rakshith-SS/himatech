import os
import re
from flask import render_template, url_for, flash, request, redirect, session
from flask.signals import got_request_exception
from sqlalchemy.orm import query
from himatech.forms import CheckOut, LoginForm, RegistrationForm, UpdateAccountInfo, AddToCart, RemoveCartItem, GoToCheckout
from datetime import datetime
from himatech import app, db, ALLOWED_EXTENSIONS
from flask_login import current_user, login_user, login_required, logout_user
from himatech.models import User, Items, Cart
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(
            f"Successfully created account for {form.username.data}", "success")
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            flash(f'{user.username} has logged in successfully', 'success')
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountInfo()
    avatar = url_for(
        'static', filename='/images/profile_pictures/'+current_user.avatar)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account is updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('account.html', form=form, avatar=avatar)


@app.route('/products', methods=['GET', 'POST'])
def product():
    form = AddToCart()
    items = Items.query.all()

    if form.validate_on_submit() and request.form.get('getId'):
        if current_user.is_authenticated is False:
            flash('Log in, To add items to Cart', 'warning')
            return redirect(url_for('login'))

        itemId = request.form.get('getId')
        cartItem = Items.query.get(itemId)
        if cartItem.product_quantity_left == 0:
            flash(f"{cartItem.product_name} is out of stock", "danger")
            return redirect(url_for('product'))
        else:
            cartItem.product_quantity_left = cartItem.product_quantity_left - 1
            cart = Cart(username=current_user.username,
                        email=current_user.email,
                        product_name=cartItem.product_name,
                        product_quantity=1,
                        product_image=cartItem.product_image,
                        product_price=cartItem.product_price
                        )

            itemExist = Cart.query.filter_by(
                username=current_user.username, product_name=cartItem.product_name).first()
            if itemExist is not None:
                cart = Cart.query.get(itemExist.cart_id)
                cart.product_quantity += 1
                cart.product_price += cartItem.product_price
                db.session.commit()

            db.session.add(cart)
            db.session.commit()
            flash(
                f"Successfully added {cartItem.product_name} to your Cart ", "success")

    return render_template('products.html', items=items, form=form)


@app.route('/cart', methods=['POST', 'GET'])
@login_required
def cart():
    form = RemoveCartItem()
    checkOut = GoToCheckout()
    cartItems = Cart.query.filter_by(
        username=current_user.username, checkout=0).all()
    cartPrice = 0
    for cartItem in cartItems:
        cartPrice += cartItem.product_price

    if cartPrice == 0:
        return render_template('cart.html', cart=cartItems, cartPrice=cartPrice)

    if form.validate_on_submit() and request.form.get('cartId'):
        cartId = request.form.get('cartId')
        cartExist = Cart.query.get(cartId)
        if cartExist is None:
            return "Nice, Tell me how you got here"
        itemName = Cart.query.get(cartId)
        product = Items.query.filter_by(
            product_name=itemName.product_name).first()
        product.product_quantity_left += itemName.product_quantity
        db.session.delete(itemName)
        db.session.commit()
        flash(
            f'{itemName.product_name} was successfully removed from your Cart', 'success')
        return redirect(url_for('cart'))

    if checkOut.validate_on_submit():
        return redirect(url_for('checkout'))

    return render_template('cart.html', cart=cartItems, cartPrice=cartPrice, form=form, checkOut=checkOut)


@app.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
    cart = Cart.query.filter_by(username=current_user.username, checkout=False).all()
    form = CheckOut()
    cartPrice = 0
    for cartItem in cart:
        cartPrice += cartItem.product_price

    if cartPrice == 0:
        return render_template('cart.html', cartPrice=cartPrice)
    
    if form.validate_on_submit():

        for item in cart:
            item.firstName = form.firstName.data
            item.lastName = form.lastName.data
            item.address = form.address.data
            item.phoneNumber = form.mobileNumber.data
            item.city = form.city.data
            item.pincode = form.pincode.data
            checkedItem = item
            db.session.add(checkedItem)
        db.session.commit()

        for item in cart:
            item.checkout = True
            checkedItem = item
            db.session.add(checkedItem)
        db.session.commit()
        flash("Shopped Successfully ", "success")
        return redirect(url_for('checkout'))
    return render_template('checkout.html', form=form, cart=cart)


@app.errorhandler(404)
def page_not_found(e):
    return "404 Error"


@app.errorhandler(401)
def unauthorised(e):
    return "401 unauthorized"
