from flask import render_template, session,redirect, request, flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import model_user
from flask_app.models import model_thought

#this one will change


bcrypt = Bcrypt(app)

#create newsomething
@app.route('/user/login', methods = ['POST'])
def user():
    #validate
    model_user.User.validator_login(request.form)
    return redirect ('/')

@app.route('/user/logout')
def logout_user():
    del session['uuid']
    return redirect('/')

#action to create in database
@app.route('/user/create', methods = ['POST'])
def user_create():
    #validations
    if not model_user.User.validator(request.form):
        return redirect('/')
    #hashing
    hash_pw = bcrypt.generate_password_hash(request.form['pw'])
    data = {
        #modifying the password
        **request.form,
        'pw' : hash_pw
    }
    #create my user and calling method
    id = model_user.User.create(data)

    #store user_id in session
    session['uuid'] = id
    return redirect('/dashboard')


#calling and displaying info
@app.route('/user/<int:id>')
def user_show(id):
    user ={
        {'id': session['user_id']}
    }
    model_user.User.get_one(id)
    return render_template('dashboard.html', user)


#calling page with form for modification on form
@app.route('/user/<int:id>/edit')
def user_edit(id):
    return render_template('user_edit.html')


# #does the editing
# @app.route('/user/<int:id>/create')
# def user_create(id):
#     return redirect('/')


# #deleting name
# @app.route('/user/<int:id>/delete')
# def user_delete(id):
#     return redirect('/')
