
# Catalog App

## About
This project show a catalog of sport items, grouped in all categories 
(previously recorded), where the user can navigate to see the items and their 
details. New item can be added when the user is logged in,
and as the item owner, only him will be able to manage it(edit or delete). 
The login used Google as security provider, so the user is going to 
be a Google user in the end.

## Demo

[![Demonstration of this application running locally](https://img.youtube.com/vi/JpHDKNTWNow/0.jpg)](https://youtu.be/JpHDKNTWNow)


## How to run this application
In order to access this web app using http://localhost:5000 URL (authorized one as it was configured on Google API), follow this procedure:
1. Install Python 3.6.5 32-bit, make sure it is in your path;
2. Install Python Flask framework v1.0.2, using pip, along with all packates listed on
"Python packages used" section; 
3. Install PostgreSQL 10 database, you will need its admin username and password later;
4. Clone this project using git, so in the end you will be at its root folder later. 
Git command: git clone https://github.com/flauberjp/CatalogApp.git;
5. Update the connection string by change the value of db_string defined on file
database_setup.py;
6. Run database_setup.py file as a python program, this will create a database
named ItemCatalogDb. Command: python .\database_setup.py;
7. Run data_seed.py file as a python program, this will create test data in the 
database. Command: python .\data_seed.py; and
8. Run app.py as a Python Flask, then access it by open http://localhost:5000 URL on your browser. Command: flask run

PS: this application connect to google auth service, so the information 
available at client_secret.json and the client_id value of the file layout.html (around line 30)
must be valid. Refer to [10] for procedures.


## Python packages used
Here is a list of some of the required packages used. For a complete list, check requirements.txt file for the completed list.
* sqlalchemy, v1.2.11
* sqlalchemy-utils, v0.33.11
* google-api-python-client, v1.7.8
* google-auth, v1.6.3
* google-auth-oauthlib, v0.3.0
* google-auth-httplib2, v0.0.3


## Routes
/, which redirects to /catalog
/catalog
/catalog/JSON
/catalog/{category_name}/items
/catalog/{category_name}/JSON
/catalog/{category_name}/{item_name}/
/catalog/{category_name}/{item_name}/edit
/catalog/{category_name}/{item_name}/delete
/catalog/{category_name}/{item_name}/JSON
/catalog/items/new
/storeauthcode, called by an ajax request actioned by Login to Google button
/logout


For item, the user shall be able to (C)reate, (U)pdate, and (D)elete only when 
logged in.

Content available in JSON format, append /JSON extension in the route.

## Files and their purposes
* database_setup.py: creates the postgreSQL database; 
* data_seed.py: create test data in the database;
* app.py: the Catalog App;
* README.md: this file with orientation about this project
* client_secret.json: files required by google in order to this application to 
their auth2 service;
* static\styles.css: custom mstyle sheet; and 
* templates\catalog: folder containing various Jinja templates used to render 
this app. 
* requirements.txt: Python packages list used by this project, generated using pip (command: 
pip freeze > requirements.txt)

And users wanting to run your project would simply run pip install -r requirements.txt to install all dependencies.

## References
1. Using PostgreSQL through SQLAlchemy. URL: < https://www.compose.com/articles/using-postgresql-through-sqlalchemy/ >. Accessed by: Mar, 27th, 2019.
2. How to create a new database using SQLAlchemy? URL: < https://stackoverflow.com/questions/6506578/how-to-create-a-new-database-using-sqlalchemy >. Accessed by: Mar, 27th, 2019.
3. Redirecting to URL in Flask. URL : < https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask >. Accessed by: Apr, 9th, 2019.
4. jsonify a SQLAlchemy result set in Flask [duplicate]. URL: < https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask >. Accessed by: Apr, 13th, 2019.
5. SQLAlchemy 1.3 Documentation, The Query Object. URL: < https://docs.sqlalchemy.org/en/latest/orm/query.html#the-query-object >. Accessed by: Apr, 13th, 2019.
6. Bootstrap 4 Examples, Framework, Jumbotron. URL: < https://getbootstrap.com/docs/4.0/examples/jumbotron/ >. Accessed by: Apr, 13th, 2019.
7. How can I get my Twitter Bootstrap buttons to right align? URL: < https://stackoverflow.com/questions/15446189/how-can-i-get-my-twitter-bootstrap-buttons-to-right-align >. Accessed by: Apr, 13th, 2019.
8. Bootstrap 4, Utilities, Display property. URL: < https://v4-alpha.getbootstrap.com/utilities/display-property/ >. Accessed by: Apr, 13th, 2019.
9. Using OAuth 2.0 for Web Server Applications . URL: < https://developers.google.com/api-client-library/python/auth/web-app >. Accessed by: Apr, 14th, 2019.
10. Authenticate with a backend server. URL: < https://developers.google.com/identity/sign-in/web/backend-auth >. Accessed by: Apr, 14th, 2019.
11. Flask Template Inheritance. URL: < http://flask.pocoo.org/docs/0.12/patterns/templateinheritance/>. Accessed by: Apr, 15th, 2019.

## License
 
The MIT License (MIT)
