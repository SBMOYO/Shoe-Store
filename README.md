# Online shoe store

#### Video Demo: https://youtu.be/3g4d0hZk5_Y

#### Description: 

Welcome to our ecommerce webstore for selling shoes!
Our ecommerce webstore is built using the Python Flask framework and allows users to browse and purchase shoes. To get started, simply log in or register on our website.

#### Getting Started:
After logging in or registering, you will be directed to the home page where you can browse our selection of shoes. If you see something you like, add it to your cart. You can view the items in your cart by clicking on the cart page. If you change your mind about an item, you can easily delete it from your cart.

When you’re ready to check out, simply follow the prompts to complete your purchase. If you ever wish to delete your account, you can do so by clicking on the delete account button. And when you’re finished shopping, don’t forget to log out by clicking on the log out button.

#### Admin Page:
As an admin user, you have access to the admin page where you can manage the products on our website. To access the admin page, simply log in with your admin credentials and navigate to the upload page where you can add more shoes from there.

#### Technical Aspects:
Our ecommerce webstore is built using the Python Flask framework. We also use Flask sessions, Werkzeug, and the tempfile library to manage user sessions and handle file uploads.

Flask is a lightweight web framework that allows us to quickly develop and deploy our website. Flask sessions provide a secure way to store user data between requests, while Werkzeug is a comprehensive WSGI web application library that we use for various utility functions. The tempfile library is used to create temporary files and directories for handling file uploads.

We have created an app.py file which contains the python code for the website and the server-side routing procedures. There are 9 routes in app.py, including the login route, register route, homepage route, upload route, admin route and other routes.

We use sqlite3 as our database. There are 4 tables in the database: kart, shoe_stock, users, and admin_user. The kart table has a many-to-many relationship with both the shoe_stock table and the users table. The admin_user table is for administration personnel who can add products into the shoe_stock table.

The website uses Jinja template formatting, so the HTML templates are stored in the templates folder. The static folder contains the style sheet and an assets folder for storing images for the website.

Thank you for choosing our ecommerce webstore for your shoe shopping needs!