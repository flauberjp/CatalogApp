#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect
from flask import url_for, jsonify, request, abort, make_response
from flask import session as login_session
from sqlalchemy import or_, and_
from database_setup import db_string, db, Category, Item, session, User
import random
import string
import json
import random
import string
from oauth2client.client import credentials_from_clientsecrets_and_code
from oauth2client.client import FlowExchangeError
from oauth2client import client
import httplib2
from apiclient import discovery

app = Flask(__name__)

app.secret_key = 'super_secret_key'


# Loggin process to Google

@app.route('/storeauthcode', methods=['POST'])
def storeauthcode():

    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF

    if not request.headers.get('X-Requested-With'):
        abort(403)

    # if request.args.get('state') != login_session['state']:
    #    print('session: different')
    #    response = make_response(json.dumps('Invalid state parameter.'), 401)
    #    response.headers['Content-Type'] = 'application/json'
    #    return response
    # print('session: same')
    # Obtain authorization code

    auth_code = request.data

    # Set path to the Web application client_secret_*.json file
    # you downloaded from the
    # Google API Console:
    # https://console.developers.google.com/apis/credentials

    CLIENT_SECRET_FILE = 'client_secret.json'

    # Exchange auth code for access token, refresh token, and ID token
    url_cred_retrieve = 'https://www.googleapis.com/auth/drive.appdata'

    credentials = credentials_from_clientsecrets_and_code(CLIENT_SECRET_FILE,
                                                          [url_cred_retrieve,
                                                           'profile', 'email'],
                                                          auth_code)

    # Get profile info from ID token

    login_session['access_token'] = credentials.access_token
    login_session['name'] = credentials.id_token['name']
    login_session['email'] = credentials.id_token['email']

    # See if a user exists, if it doesn't make a new one
    userId = getUserID(login_session['email'])
    if userId is None:
        userId = createUser(login_session)
    
    user = getUserInfo(userId)

    print('User logged in: \n' +
             '\t  Name: ' + user.name + '\n' + 
             '\tE-mail: ' + user.email + '\n')

    response = make_response(json.dumps('OAuth code stored.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def createUser(login_session):
    newUser = User(name=login_session['name'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user

# Perfor logout

@app.route('/logout')
def showLogout():
    access_token = login_session['access_token']
    if access_token is not None:
        del login_session['access_token']
        del login_session['name']
        del login_session['email']

    return redirect(url_for('showCatalog'))


@app.route('/')
def redirectToShowCatalog():
    return showCatalog()


# Show the catalog categories

@app.route('/catalog', methods=['GET'])
def showCatalog():
    loggedIn = 'access_token' in login_session \
        and login_session['access_token'] is not None
    userId = None
    if loggedIn:
        userId = getUserID(login_session['email'])

    categories = session.query(Category).all()
    items = session.query(Item).join(Category).limit(8)
    loggedIn = 'access_token' in login_session \
        and login_session['access_token'] is not None
    name = ''
    if loggedIn:
        name = login_session['name']
    return render_template('catalog/catalog.html',
                           categories=categories, items=items,
                           loggedIn=loggedIn, name=name)


# Equivalent of method showCatalog()
# but showing the result in JSON format

@app.route('/catalog/JSON', methods=['GET'])
def showCatalogJSON():
    categories = session.query(Category).all()

    return jsonify(categories = [i.serialize for i in categories])


# Show all items from a category
# For the special case where item_name is equal to 'items', then
# show only the details of that item.

@app.route('/catalog/<string:category_name>/<string:item_name>',
           methods=['GET'])
def showItems(category_name, item_name):
    loggedIn = 'access_token' in login_session \
            and login_session['access_token'] is not None
    name = ''
    items = None
    userId = None
    if loggedIn:
        name = login_session['name']
        userId = getUserID(login_session['email'])

    if item_name == 'items':
        categories = session.query(Category).all()
        
        items = session.query(Item).join(Category).filter(Category.name ==
                                                            category_name
                                                            )        

        return render_template(
            'catalog/itemsByCategory.html',
            selected_category_name=category_name,
            categories=categories,
            items=items,
            loggedIn=loggedIn,
            name=name,
            )
    else:
        item = session.query(Item).join(Category).filter(Category.name ==
                                                        category_name,
                                                        Item.name == 
                                                        item_name
                                                        ).first()

        enable_edit_and_delete_buttons = (loggedIn == 
                                          True) and (item.user is None or  
                                                     item.user.id == userId)
        return render_template('catalog/itemDetails.html',
                               category_name=category_name, item=item,
                               loggedIn=loggedIn, name=name,
                               enable_edit_and_delete_buttons=enable_edit_and_delete_buttons)


# Create an Item

@app.route('/catalog/items/new', methods=['GET', 'POST'])
def newItem():
    loggedIn = 'access_token' in login_session \
        and login_session['access_token'] is not None
    name = ''
    user_email = ''
    if loggedIn:
        name = login_session['name']
        user_email = login_session['email']

    if request.method == 'POST':
        if loggedIn == False and user_email == request.form['user_email']:
            abort(403)

        userId = getUserID(request.form['user_email'])

        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category_id=request.form['category_id'],
                       user_id=userId)
        session.add(newItem)
        session.commit()
        category = session.query(Category).filter(Category.id ==
                                                  request.form['category_id']
                                                  ).first()
        return redirect(url_for('showItems',
                        category_name=category.name,
                        item_name=request.form['name']))
    else:
        categories = session.query(Category).all()
        return render_template('catalog/newItem.html',
                               categories=categories,
                               loggedIn=loggedIn,
                               name=name,
                               user_email=user_email)


# Edit an Item

@app.route('/catalog/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    loggedIn = 'access_token' in login_session \
                and login_session['access_token'] is not None
    name = ''
    user_email = ''
    if loggedIn:
        name = login_session['name']
        user_email = login_session['email']
        
    item = session.query(Item).join(Category).filter(Category.name ==
                                                     category_name,
                                                     Item.name == item_name
                                                     ).first()
    if request.method == 'POST':
        if loggedIn == False and user_email == request.form['user_email']:
            abort(403)
        item.name = request.form['name']
        item.description = request.form['description']
        item.category_id = request.form['category_id']
        session.add(item)
        session.commit()
        category = session.query(Category).filter(Category.id ==
                                                  item.category_id).first()
        return redirect(url_for('showItems',
                        category_name=category.name,
                        item_name=item.name))
    else:
        categories = session.query(Category).all()

        return render_template(
            'catalog/editItem.html',
            categories=categories,
            category_name=category_name,
            item_name=item_name,
            item=item,
            loggedIn=loggedIn,
            name=name,
            user_email=user_email
            )


# Delete Item

@app.route('/catalog/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    loggedIn = 'access_token' in login_session \
        and login_session['access_token'] is not None    
    name = ''
    user_email = ''
    if loggedIn:
        name = login_session['name']
        user_email = login_session['email']

    itemToDelete = session.query(Item).join(Category).filter(Category.name ==
                                                             category_name,
                                                             Item.name ==
                                                             item_name).first()
    if request.method == 'POST':
        if loggedIn == False and user_email == request.form['user_email']:
            abort(403)
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems',
                        category_name=category_name, item_name='items'))
    else:
        return render_template('catalog/deleteItem.html',
                               category_name=category_name,
                               item_name=item_name, loggedIn=loggedIn,
                               name=name,
                               user_email=user_email)


# Equivalent of the method showItems(category_name, item_name),
# but showing the result in JSON format

@app.route('/catalog/<string:category_name>/<string:item_name>/JSON',
           methods=['GET'])
def showItemsJSON(category_name, item_name):
    loggedIn = 'access_token' in login_session \
            and login_session['access_token'] is not None
    userId = None
    if loggedIn:
        userId = getUserID(login_session['email'])

    category = session.query(Category).filter(Category.name == category_name
                                              ).first()
    if item_name == 'items':
        items = session.query(Item).filter(Item.category_id ==
                                           category.id)
        items_to_JSONinfy=[i.serialize for i in items]
        return jsonify(items_to_JSONinfy)
    else:
        item = session.query(Item).filter(Item.category_id == category.id,
                                          Item.name == item_name
                                          ).first()
        return jsonify(item.serialize)
