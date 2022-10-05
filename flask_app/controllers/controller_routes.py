from flask import render_template, session,redirect, request, flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import model_thought

#this one will change
from flask_app.models import model_user

@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    return render_template('index.html')

#checking if someone is logged in
@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    #context will be able to call all recipes
    user_data ={
        'id': session['uuid']
    }
    #user_data is defined to access session id in dashboard html
    context = {
        'all_thoughts': model_thought.Thought.get_all(),
        'user': model_user.User.get_one(user_data)
        
    }
    return render_template('dashboard.html', **context)