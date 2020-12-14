from flask import(Blueprint, flash, g, redirect, render_template, url_for, request)
from werkzeug.exceptions import abort
from flaskr.auth import login_required

from flaskr.db import get_db

bp = Blueprint('blog', __name__)

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
