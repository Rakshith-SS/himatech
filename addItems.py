#!/usr/bin/env python3
from himatech.models import db, Items

product_name = input("Enter a product name: ")
product_desc = input("Give the Product Description: ")
product_price = input("Price of the product: ")
image1  = input("Product image1 [hard_disk.jpg] :")
image2 = input("Product image2 :")
image3 = input("Product image3 :")
product_sold_totally = input("Product sold totally[default-0]: ")
category = input("Product Category: ")
year_of_manufacture = input("Year of Manufacture: ")
warranty = input("Product Warranty: ")
model_number = input("Model Number: ")
discount_percent = input("Enter discount percentage: ")
discount_price = input("Enter discount price: ")
specification1 = input("Feature1 : ")
specification_value1 = input("Value1 : ")
specification2 = input("Feature2 : ")
specification_value2 = input("Value2 : ")
specification3 = input("Feature3 : ")
specification_value3 = input("Value3 : ")
specification4 = input("Feature4 : ")
specification_value4 = input("Value4 : ")
company = input("Company : ")
item = Items(
            product_name=product_name,
            product_desc=product_desc,
            product_price=product_price,
            product_images={
                'image1': image1,
                'image2': image2,
                'image3': image3
                },
            product_sold_totally=product_sold_totally,
            category=category,
            year_of_manufacture=year_of_manufacture,
            warranty=warranty,
            model_number=model_number,
            discount_percent= discount_percent,
            specifications = { specification1: specification_value1,
                               specification2 : specification_value2,
                               specification3 : specification_value3,
                               specification4 : specification_value4 
                            },
            company = company
            )
db.session.add(item)
db.session.commit()
print(f'{product_name} was added Successfully to our database....')
