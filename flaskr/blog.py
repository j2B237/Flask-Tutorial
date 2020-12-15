from flask import(Blueprint, flash, g, redirect, render_template, url_for, request)
from werkzeug.exceptions import abort
from flaskr.auth import login_required

from flaskr.db import get_db

#-- Define new blueprint for the blog ----------#
bp = Blueprint('blog', __name__)

#-------- URL for index ------------#
@bp.route('/')
def index():

    "Display all the posts"
    #initialize connection to database
    db = get_db()

    #execute query in order to display all posts associated to the current user
    posts = db.execute(
        "SELECT * FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC"
        ).fetchall()
    return render_template("blog/index.html", posts = posts)

#-------- Url for create new post --------------#
@bp.route('/create', methods = ['POST','GET'])
@login_required
def create():
    "Create a new post"
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title :
            error = "Title is required"
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES(?, ?, ?) ", (title, body, g.user['id'])
                )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')
    
#--------- Search for a post -----------------#
def get_post(id, check_author=True):
    "Search for a post and check if the author matches to the current user "

    db = get_db()
    post = db.execute(
        "SELECT * FROM post p JOIN user u ON  p.author_id = u.id  WHERE p.id = ? ", (id,)
        ).fetchone()

    if post is None:
        abort(404, "post {} does'nt exist".format(id))
    if check_author and post['author_id'] != g.user['id']:
        abort(403)  
        
    return post


#---------- Url for update existing post ----------#
@bp.route('/<int:id>/update', methods = ['POST','GET'])
def update(id):
    "Update a post "
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Title is required"
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ? , body = ? WHERE id = ?", (title, body, id)
                )
            db.commit() 
        return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post = post)

#------------- Url for delete a post ----------------------#
@bp.route('/<int:id>/delete', methods = ['POST'])
def delete(id):
    post = get_post(id)
    db = get_db()
    if post is None:
        abort(404, "post {} does'nt exist".format(id))
    else:
        db.execute(
            "DELETE FROM post WHERE id= ?", (id,)
            )
        db.commit()
    return redirect(url_for('blog.index'))
