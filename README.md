# Himatech

**Contents**

<a href="#about">About</a><br>
<a href="#technologies-used">Technologies Used</a><br>
<a href="#features">Features</a><br>
<a href="#credits">Credits</a><br>

## About

An e-commerce web-app project developed using flask, where an end-user can register, login into their account,
add products to their cart or wishlist and view their purchased items

## Technologies Used

+ Flask
+ SQL(SQLite for development)
+ Javascript
+ HTML/CSS
+ Git - for version control

## Features

+ **Dynamic Routes**<br>

	Creating Dynamic routes for products based on their categories, which is retrieved from a backend database.

	**Code**

	![Dynamic Routes Code](docs/dynamic_routes_code.png)

	**Output**

	![Dynamic Routes](docs/dynamic_routes.png)

+ **Login and Register System**

	An end user can login and Register, and all user inputs are validated

	![Login and Register System](docs/signup_page.png)

	**Validation**

	![Login and Register](docs/validating_fields.png)

+ **Wishlist and Cart Page**

	Adding, removing and clearing cart in wishlist and cart pages

	**Wishlist Page**

	![Wishlist](docs/wishlist_page.png)

 	**Cart Page**

	![Cart Page](docs/cart_page.png)

	Adding a product, to cart through wishlist, on doing so renders a flash message

	![Wishlist Action](docs/wishlist_page_action.png)

	Removing a product from a cart

	![Removing Product](docs/removing_product.png)

+ **Product Detail**

	A description of each product, that is retrieved from a database

	**code snippet**

	![Product Detail](docs/product_detail_code.png)

	**Output**

	![Product Detail](docs/product_detail.png)

+ **Checkout Page**

	Billing page

	![Checkout Page](docs/checkout_form.png)

+ **Orders Page**

	An end-user can, view their orders

	![Orders](docs/orders_page.png)


## Running the web-app

+ In order to run this web-app, python3 must be installed

1. Clone the repo using git and cd into the repo

```
git clone https://github.com/Rakshith-SS/himatech.git

cd himatech
```

2. Install the python requirements via pip

``` python
python3 -m pip install -r requirements.txt
```

3. Running the web-app.

```python
python run.py
```

## Credits

Thanks [Sagar](https://github.com/sagar-sagar) and [Vishwas](https://github.com/vvs2001) for contributing to the front-end work
