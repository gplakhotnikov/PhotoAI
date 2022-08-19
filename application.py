import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, image_save, sketch, filters, noise_reduction, enhancement

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/studio", methods=["GET", "POST"])
def studio():
    if request.method == "GET":
        return render_template("studio_add.html")
    else:
        if not request.form.get("URL"):
            return render_template("error.html", string_out='Enter a valid URL')

        url = request.form.get("URL")
        feedback = image_save(url)
        print("FEEDBACK:", feedback)
        if feedback == 'Invalid URL or unsupported file format':
            return render_template("error.html", string_out=feedback)
        else:
            flash('The image has been added')
            return render_template("studio.html")


@app.route("/return_function")
def return_function():
    return render_template("studio.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        if not (request.form.get("name")):
            return render_template("error.html", string_out='Provide your name')
        elif not (request.form.get("email")):
            return render_template("error.html", string_out='Provide your email')
        elif not (request.form.get("message")):
            return render_template("error.html", string_out='Type the message')
        else:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

        db.execute("INSERT INTO messages (name, email, message) VALUES (:name, :email, :message)",
                        name=name, email=email, message=message)

        flash('Your message has been sent')
        return render_template("index.html")

@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "GET":
        return render_template("error.html", string_out='Nothing to show here')
    else:
        action = request.form.get("action")

    if action == 'sketch':
        sketch('static/uploads/out.jpg')
    elif action == 'noise':
        noise_reduction()
    elif action == 'blur':
        filters('blur')
    elif action == 'contour':
        filters('contour')
    elif action == 'detail':
        filters('detail')
    elif action == 'edge_enhance':
        filters('edge_enhance')
    elif action == 'edge_enhance_more':
        filters('edge_enhance_more')
    elif action == 'emboss':
        filters('emboss')
    elif action == 'find_edges':
        filters('find_edges')
    elif action == 'sharpen':
        filters('sharpen')
    elif action == 'smooth':
        filters('smooth')
    elif action == 'smooth_more':
        filters('smooth_more')
    elif action == 'color':
        enhancement('color')

    return render_template("result.html")


@app.route("/messages")
@login_required
def messages():
    messages = db.execute("SELECT * FROM messages")
    return render_template("messages.html", messages=messages)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/messages")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
