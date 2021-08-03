import os
import secrets
from flask import render_template, url_for, flash, request, redirect
from himatech.forms import (CheckOut, LoginForm,
                            RegistrationForm, UpdateAccountInfo,
                            RemoveCartItem, GoToCheckout,
                            CancelOrder, WishlistAddToCart,
                            ChangeProfilePicture
                            )
from datetime import datetime, timedelta
from himatech import app, db
from flask_login import current_user, login_user, login_required, logout_user
from himatech.models import User, Items, Cart, Wishlist
from markupsafe import escape

PROFILES_PICTURES = os.getcwd() + '/himatech/static/images/profile_pictures/'


@app.route('/')
@app.route('/home')
def index():
    item_category = []
    category_image = []
    items = Items.query.all()
    for item in items:
        item_category.append(item.category)
    groups = set(item_category)
    for group in groups:
        images = Items.query.filter_by(category=group).first()
        category_image.append(images.product_images['image1'])

    category = dict(zip(groups, category_image))
    return render_template('index.html', category=category)


@app.route('/signUpLogin', methods=['POST', 'GET'])
def signUpLogin():
    registerForm = RegistrationForm()
    loginForm = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if registerForm.validate_on_submit() and request.form.get('register'):
        user = User(
            username=registerForm.username.data,
            email=registerForm.email.data,
            phonenumber=registerForm.mobileNumber.data
            )
        user.set_password(registerForm.password.data)
        db.session.add(user)
        db.session.commit()
        flash(
                f"""Successfully created
                account for {registerForm.username.data}""",
                "success")
        return redirect(url_for('index'))
    if loginForm.validate_on_submit() and request.form.get('login'):
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user is None or not user.check_password(loginForm.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('signUpLogin'))
        else:
            login_user(user, remember=loginForm.remember_me.data)
            flash(f'{user.username} has logged in successfully', 'success')
            return redirect(url_for('index'))
    return render_template(
                            'signUPLogIn.html',
                            registerForm=registerForm,
                            loginForm=loginForm
                            )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# validates an image, generates a random name for the uploaded image and
# saves it to "profile_pictures" directory
def savePicture(Picture):
    """
    Goes to the zeroth byte,
    during the file size validation goes to the last byte
    and when saved renders an image of zero bytes lolXD
    """
    Picture.seek(0)
    picture = Picture.filename
    ext = os.path.splitext(picture)[1]
    image = secrets.token_hex(5) + ext
    Picture.save(PROFILES_PICTURES + image)
    return image


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountInfo()
    changePhoto = ChangeProfilePicture()
    avatar = url_for(
                    'static',
                    filename='/images/profile_pictures/'+current_user.avatar
                    )
    if changePhoto.validate_on_submit() and request.form.get('pictureField'):
        picture = savePicture(changePhoto.picture.data)
        if current_user.avatar != "default.jpg":
            oldPicture = current_user.avatar
            imagePath = PROFILES_PICTURES + oldPicture
            os.remove(imagePath)
        current_user.avatar = picture
        db.session.commit()
        flash("Updated Profile Picture Successfully!", "success")
        return redirect(url_for('account'))
    if form.validate_on_submit() and request.form.get('allFields'):
        cartName = Cart.query.filter_by(
                                        username=current_user.username,
                                        email=current_user.email
                                        ).all()
        wishlistName = Wishlist.query.filter_by(

                                                username=current_user.username,
                                                email=current_user.email
                                                ).all()
        if cartName is not None:
            for name in cartName:
                name.username = form.username.data
                name.email = form.email.data
                db.session.commit()
        if wishlistName is not None:
            for name in wishlistName:
                name.username = form.username.data
                name.email = form.email.data
                db.session.commit()
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Successfully Updated account!', 'success')
        return redirect(url_for('index'))
    return render_template(
                            'editprofile.html',
                            form=form,
                            changePhoto=changePhoto,
                            avatar=avatar
                        )


@app.route('/<category>', methods=['GET', 'POST'])
def product_category(category):
    items = Items.query.filter_by(category=escape(category)).all()
    if len(items) == 0:
        return render_template('404.html')
    else:
        itemStock = []
        # stock of an item
        for item in items:
            itemName = Items.query.filter_by(
                                            product_name=item.product_name
                                            ).first()
            if itemName.product_quantity_left > 0:
                itemStock.append("In Stock")
            else:
                itemStock.append("Not Available")
        # Adding to Wishlist
        if request.method == "POST" and request.form.get('product_id'):
            if current_user.is_authenticated is False:
                flash('Log in, to add items to your Wishlist', 'warning')
                return redirect(url_for('signUpLogin'))
            productId = request.form.get('product_id')
            product = Items.query.get(productId)
            if product is None:
                return "Nice Please Tell Me, How you did this"
            # check if the item is  already present on the wishlist
            productName = product.product_name
            productImage = product.product_images['image1']
            productPrice = product.product_price
            isItemOnWishlist = Wishlist.query.filter_by(
                                                        username=current_user.username,
                                                        wishlist_item=productName
                                                        ).first()
            if isItemOnWishlist:
                flash('Item has Already Been added to Your Wishlist', 'info')
            else:
                # Add item to Wishlist
                wishlist = Wishlist(
                                    username=current_user.username,
                                    email=current_user.email,
                                    wishlist_item=productName,
                                    wishlist_image=productImage,
                                    wishlist_item_price=productPrice
                                    )
                db.session.add(wishlist)
                db.session.commit()
                flash(
                        f'{productName} is added to your wishlist',
                        'success'
                    )
                return redirect(url_for('index'))
        # Adding to Cart
        if request.method == 'POST' and request.form.get('getId'):
            if current_user.is_authenticated is False:
                flash('Log in, to add items to your cart', 'warning')
                return redirect(url_for('signUpLogin'))
            itemId = request.form.get('getId')
            cartItem = Items.query.get(itemId)
            if cartItem is None:
                return "Nice Tell Me How you, Got here"
            if cartItem.product_quantity_left <= 0:
                flash(f"{cartItem.product_name} is out of stock", "danger")
                return redirect(url_for('index'))
            else:
                cartItem.product_quantity_left -= 1
                cartItem.product_sold_totally += 1
                cart = Cart(username=current_user.username,
                            email=current_user.email,
                            product_name=cartItem.product_name,
                            product_quantity=1,
                            product_image=cartItem.product_images['image1'],
                            product_price=cartItem.product_price,
                            checkout=False
                            )
                itemExist = Cart.query.filter_by(
                                                username=current_user.username,
                                                product_name=cartItem.product_name,
                                                checkout=False
                                                ).first()
                # if an item already exists in Cart
                if itemExist is not None:
                    cart = Cart.query.get(itemExist.cart_id)
                    cart.product_quantity += 1
                    cart.product_price += cartItem.product_price
                    db.session.commit()
                db.session.add(cart)
                db.session.commit()
                flash(f"Successfully added {cartItem.product_name} to your Cart ", "success")
        return render_template(
                                'product.html',
                                items=items,
                                itemStock=itemStock
                            )


@app.route('/productinfo/<productName>', methods=['GET', 'POST'])
def productinfo(productName):
    title = escape(productName)
    item = Items.query.filter_by(
                                product_name=escape(productName)
                                ).first_or_404()
    # Check up on item stock
    if item.product_quantity_left > 0:
        itemStock = "In Stock"
    else:
        itemStock = "Not Available"
    # adding items to Cart
    if request.method == 'POST' and request.form.get('addToCart'):
        item = Items.query.get(request.form.get('addToCart'))
        if current_user.is_authenticated is False:
            flash(f'Login, to add {item.product_name} to your cart', 'warning')
            return redirect(url_for('signUpLogin'))
        item.product_quantity_left -= 1
        item.product_sold_totally += 1
        cart = Cart(username=current_user.username,
                    email=current_user.email,
                    product_name=item.product_name,
                    product_quantity=1,
                    product_image=item.product_images['image1'],
                    product_price=item.product_price,
                    checkout=False
                    )
        itemExist = Cart.query.filter_by(
                                        username=current_user.username,
                                        product_name=item.product_name,
                                        checkout=False
                                        ).first()
        # if an item already exists in Cart for a particular user
        if itemExist is not None:
            cart = Cart.query.get(itemExist.cart_id)
            cart.product_quantity += 1
            cart.product_price += item.product_price
            db.session.commit()
        db.session.add(cart)
        db.session.commit()
        flash(f"Successfully added {item.product_name} to your Cart ", "success")
    # Adding items to your wishlist
    if request.method == 'POST' and request.form.get('addToWishlist'):
        item = Items.query.get(request.form.get('addToWishlist'))
        if current_user.is_authenticated is False:
            flash(f'Log in, to add {item.product_name} to your Wishlist', 'warning')
            return redirect(url_for('signUpLogin'))
        # check if the item is  already present on the wishlist
        productName = item.product_name
        productImage = item.product_images['image1']
        productPrice = item.product_price
        isItemOnWishlist = Wishlist.query.filter_by(
                            username=current_user.username,
                            wishlist_item=productName
                           ).first()
        # check if an item is already present is already
        # present in Wishlist for the logged in user
        if isItemOnWishlist:
            flash('Item has Already Been added to Your Wishlist', 'info')
        else:
            # Add item to Wishlist
            wishlist = Wishlist(
                                username=current_user.username,
                                email=current_user.email,
                                wishlist_item=productName,
                                wishlist_image=productImage,
                                wishlist_item_price=productPrice
                                )
            db.session.add(wishlist)
            db.session.commit()
            flash(f'{productName} is successfully added to your wishlist', 'success')
            return redirect(url_for('index'))
    return render_template(
                            'productdetail.html',
                            item=item,
                            itemStock=itemStock,
                            title=title
                        )


@app.route('/cart', methods=['POST', 'GET'])
@login_required
def cart():
    form = RemoveCartItem()
    checkOut = GoToCheckout()
    cartItems = Cart.query.filter_by(
                                    username=current_user.username,
                                    checkout=False
                                    ).all()
    # Removing an item quantity from your Cart
    if request.method == 'POST' and request.form.get('itemMinus'):
        cartItem = Cart.query.get(request.form.get('itemMinus'))
        if cartItem is None:
            return "Nice Tell me, how you got here"
        if cartItem.product_quantity == 1:
            db.session.delete(cartItem)
            product = Items.query.filter_by(
                                            product_name=cartItem.product_name
                                            ).first()
            product.product_quantity_left += 1
            db.session.commit()
            flash(f"{cartItem.product_name} was successfully removed from your Cart", "info")
            return redirect(url_for('cart'))
        itemPrice = cartItem.product_price/cartItem.product_quantity
        cartItem = Cart.query.get(request.form.get('itemMinus'))
        cartItem.product_quantity -= 1
        cartItem.product_price -= itemPrice
        # Making Changes to item quantity
        product = Items.query.filter_by(product_name=cartItem.product_name).first()
        product.product_quantity_left += 1
        db.session.commit()
        return redirect(url_for('cart'))
    # Increasing an item quantity from your cart
    if request.method == 'POST' and request.form.get('itemPlus'):
        cartItem = Cart.query.get(request.form.get('itemPlus'))
        itemName = Items.query.filter_by(product_name=cartItem.product_name).first()
        if cartItem is None:
            return "Nice Tell me, how you got here"
        if itemName.product_quantity_left <= 0:
            flash(f"{cartItem.product_name} is no longer available in stock", "info")
            return redirect(url_for('cart'))
        else:
            itemPrice = cartItem.product_price/cartItem.product_quantity
            cartItem = Cart.query.get(request.form.get('itemPlus'))
            cartItem.product_quantity += 1
            cartItem.product_price += itemPrice
            # Making changes to item quantity
            product = Items.query.filter_by(
                                            product_name=cartItem.product_name
                                            ).first()
            product.product_quantity_left -= 1
            db.session.commit()
            return redirect(url_for('cart'))
    # deleting an item from your cart
    if request.method == 'POST' and request.form.get('cartId'):
        cartId = request.form.get('cartId')
        cartExist = Cart.query.get(cartId)
        if cartExist is None:
            return "Nice, Tell me how you got here"
        # Making changes to item quantity
        itemName = Cart.query.get(cartId)
        product = Items.query.filter_by(
                                        product_name=itemName.product_name
                                        ).first()
        product.product_quantity_left += itemName.product_quantity
        db.session.delete(itemName)
        db.session.commit()
        flash(f'{itemName.product_name} was successfully removed from your Cart', 'success')
        return redirect(url_for('cart'))

    # clearing your cart
    if request.method == 'POST' and request.form.get('clearCart'):
        for item in cartItems:
            itemName = Items.query.filter_by(product_name=item.product_name).first()
            itemName.product_quantity_left += item.product_quantity
            db.session.commit()
            db.session.delete(item)
        db.session.commit()
        flash("Your Cart was cleared successfully!", "success")
        return redirect(url_for('cart'))
    cartPrice = 0
    for cartItem in cartItems:
        cartPrice += cartItem.product_price
    if cartPrice == 0:
        return render_template('emptycart.html')
    return render_template(
                            'mycart.html',
                            cart=cartItems,
                            cartPrice=cartPrice,
                            form=form,
                            checkOut=checkOut
                            )


@app.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
    cart = Cart.query.filter_by(
                                username=current_user.username,
                                checkout=False
                                ).all()
    totalCartItems = len(cart)
    form = CheckOut()
    cartPrice = 0
    for cartItem in cart:
        cartPrice += cartItem.product_price
    if cartPrice == 0:
        return render_template('emptycart.html')
    if form.validate_on_submit():
        for item in cart:
            item.firstName = form.firstName.data
            item.lastName = form.lastName.data
            item.address = form.address.data
            item.phoneNumber = form.mobileNumber.data
            item.city = form.city.data
            item.pincode = form.pincode.data
            item.checkoutTime = datetime.now().replace(microsecond=0)
            item.invoiceNumber = secrets.token_hex(3)
            checkedItem = item
            db.session.add(checkedItem)
        db.session.commit()
        for item in cart:
            item.checkout = True
            checkedItem = item
            db.session.add(checkedItem)
        db.session.commit()
        flash("Shopped Successfully ", "success")
        return redirect(url_for('index'))
    return render_template(
                            'checkout.html',
                            form=form,
                            cart=cart,
                            cartPrice=cartPrice,
                            totalCartItems=totalCartItems
                            )


@app.route('/orders', methods=["GET", "POST"])
@login_required
def orders():
    form = CancelOrder()
    orders = Cart.query.filter_by(
                                    email=current_user.email,
                                    checkout=True
                                ).all()
    checkedOutTime = []
    shoppedItems = []
    orderedPrice = 0
    TotalPrice = []
    DeliveryDate = []
    for item in orders:
        if item.checkoutTime not in checkedOutTime:
            checkedOutTime.append(item.checkoutTime)
    for orderedTime in checkedOutTime:
        orderedItems = Cart.query.filter_by(
                                            email=current_user.email,
                                            checkout=True,
                                            checkoutTime=orderedTime
                                            ).all()
        shoppedItems.append(orderedItems)
        DeliveryDate.append(orderedTime + timedelta(days=3))
    # total price when more than two products are ordered at the same time
    for items in shoppedItems:
        if len(items) > 1:
            for item in items:
                orderedPrice += item.product_price
            TotalPrice.append(orderedPrice)
            orderedPrice = 0
        else:
            for item in items:
                TotalPrice.append(item.product_price)
    itemCount = len(DeliveryDate)
    if request.method == 'POST':
        flash("Your cancellation request has been considered and will be removed shortly", 'info')
    if len(orders) == 0:
        return render_template('emptyorder.html')
    return render_template(
                            'myorders.html',
                            shoppedItems=shoppedItems,
                            form=form,
                            DeliveryDate=DeliveryDate,
                            TotalPrice=TotalPrice,
                            itemCount=itemCount,
                            checkedOutTime=checkedOutTime
                            )


@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
    addToCart = WishlistAddToCart()
    wishlist = Wishlist.query.filter_by(username=current_user.username).all()
    itemStock = []

    for item in wishlist:
        itemName = Items.query.filter_by(
                product_name=item.wishlist_item
                ).first()
        if itemName.product_quantity_left > 0:
            itemStock.append("In Stock")
        else:
            itemStock.append("Not Available")
    # add an Item from wishlist to a user's cart
    if request.method == 'POST' and request.form.get('addToCart'):
        item = Items.query.filter_by(
                                    product_name=request.form.get('addToCart')
                                    ).first()
        wishlistItem = Wishlist.query.get(request.form.get('addToCartId'))
        # check if the item is an instance of the class Items
        if isinstance(item, Items):
            item.product_quantity_left -= 1
            if item.product_quantity_left <= 0:
                flash(f"{item.product_name} is out of stock", "danger")
                return redirect(url_for('wishlist'))
            else:
                cart = Cart(username=current_user.username,
                            email=current_user.email,
                            product_name=item.product_name,
                            product_quantity=1,
                            product_image=item.product_images['image1'],
                            product_price=item.product_price,
                            checkout=False
                            )
                itemPresent = Cart.query.filter_by(username=current_user.username, product_name = item.product_name, checkout=False).first()
                if itemPresent is not None:
                    cart = Cart.query.get(itemPresent.cart_id)
                    cart.product_quantity += 1
                    cart.product_price += itemPresent.product_price
                    db.session.commit()
                db.session.add(cart)
                db.session.delete(wishlistItem)
                db.session.commit()
                flash(f'Successfully added {item.product_name} to your Cart', 'success')
                return redirect(url_for('wishlist'))
        else:
            return "Tell How You got to Wishlist"

    # remove an Item from a user's wishlist
    if request.method == 'POST' and request.form.get('removeItemId'):
        wishlistItem = Wishlist.query.get(request.form.get('removeItemId'))
        db.session.delete(wishlistItem)
        db.session.commit()
        flash(f'{wishlistItem.wishlist_item} was removed from your wishlist successfully! ', 'info')
        return redirect(url_for('wishlist'))

    # clear a user's wishlist
    if request.method == 'POST' and request.form.get('clearWishlist'):
        for item in wishlist:
            db.session.delete(item)
        db.session.commit()
        flash("Your Wishlist was successfully cleared!", "info")
        return redirect(url_for('wishlist'))

    if len(wishlist) == 0:
        return render_template('emptywishlist.html')

    return render_template(
                            'wishlist.html',
                            wishlist=wishlist,
                            itemStock=itemStock,
                            addToCart=addToCart
                        )
# Error Pages


@app.errorhandler(401)
def unauthorised(e):
    return render_template('401.html')


@app.errorhandler(403)
def ForbiddenError(e):
    return render_template('403.html')


@app.errorhandler(404)
def PageNotFound(e):
    return render_template('404.html')
