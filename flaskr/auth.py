import functools
from flask import(Blueprint, flash, g, redirect, render_template, session, url_for, request)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

#---------------------------------------------------#

@bp.route('/register', methods = ['GET', 'POST'])
def register():

    "Register a new user to the blog "
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if not username :
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif db.execute(
            "SELECT id from user WHERE username = ?",(username, )).fetchone() is not None:
            error = "User {} is already registered ".format(username)
        if error is None:
            db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)", (username, generate_password_hash(password))
                    )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
    #else request.method == 'GET'
    return render_template('auth/register.html')


#---------------------------------------------------#
@bp.route('/login', methods = ['GET','POST'])
def login():
    
    "Use to authenticate user "
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute(
                "SELECT * FROM user WHERE username = ?",(username,)
                ).fetchone()
        
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password"
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


#---------------------------------------------------#
@bp.before_app_request
def load_logged_in_user():
    
    "function that runs before the view function, no matter what URL is requested"
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
                "SELECT * FROM user WHERE id = ?",(user_id,)
                ).fetchone()



#---------------------------------------------------#
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



#---------------------------------------------------#
def login_required(view):
    
    "Creating, editing, and deleting blog posts will require a user to be logged in"
    @functools.wraps(view)
    
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view
