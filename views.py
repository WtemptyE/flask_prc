from app import app

from flask import render_template  # Support template and request
from flask import request

from flask import flash, redirect, request, url_for

from flask_login import login_user

from app import login_manager
from forms import LoginForm

@app.route('/')
def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    if not name:
        name = '<unknown>'
    return render_template('homepage.html', number=number, name=name)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember=form.remember_me.data)
            flash("Successfully logged in as %s." % form.user.email, "success")
            return redirect(request.args.get("next") or url_for("homepage"))
    else:
        form = LoginForm()
        return render_template("login.html", form=form)

from flask_login import login_user, logout_user
@app.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(request.args.get('next') or url_for('homepage'))