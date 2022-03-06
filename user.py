from flask import Blueprint, render_template, flash
from flask import redirect, url_for, request, session

from models import db, Users

from forms import LoginForm
from forms import RegisterForm
from forms import ChangePassword

from utils import login_required

user = Blueprint("user", __name__)

@user.route("/settings/<username>/")
@login_required
def user_settings(username):
    if username == session["logged"]:
        user = Users.query.filter_by(username=username).first()

        if user:
            form = RegisterForm()
            form.email.data = user.email
            form.username.data = user.username
            form.password.data = ""
            subscribe = user.subscribe

            return render_template("User/user_settings.html", form=form, sub=subscribe)
    
    return render_template("errors/404.html")

@user.route("/settings/<username>/", methods=["POST"])
@login_required
def change_user_settings(username):
    user = Users.query.filter_by(username=username).first()
    form = RegisterForm()

    if request.method == "POST":
        check = request.form.get("check")

        if check != user.subscribe:
            user.subscribe = check
            db.session.add(user)
            db.session.commit() 

    if user and form.validate():
        if form.password.data != "" and user.check_password(form.password.data):
            old_email = user.email
            new_email = form.email.data
            
            if old_email != new_email:
                user.email = new_email
                db.session.add(user)
                db.session.commit()

            old_username = user.username
            new_username = form.username.data
            
            if old_username != new_username:

                all_users = [user.username for user in Users.query.all()]
                if new_username not in all_users:
                    username = new_username
                    session["logged"] = username

                    user.username = new_username
                    db.session.add(user)
                    db.session.commit()
        
    return redirect(url_for("user.user_settings", username=username))

@user.route("/login/", methods=["GET"])
def view_login():
    log_form = LoginForm()
    return render_template("User/login.html", form=log_form)

@user.route("/login/", methods=["POST"])
def user_login():
    log_form = LoginForm()
    if log_form.validate():
        
        obj_user = Users.query.filter_by(username=log_form.username.data).first()
        if obj_user:
            
            if obj_user.check_password(log_form.password.data):
                session["logged"] = log_form.username.data
                return redirect(url_for("article.view_home"))
            else:
                return render_template("User/login.html", form=log_form)

    return redirect(url_for("user.view_login"))

@user.route("/register/", methods=["GET"])
def view_register():
    reg_form = RegisterForm()
    return render_template("User/register.html", form=reg_form)

@user.route("/register/", methods=["POST"])
def user_register():
    check = False
    reg_form = RegisterForm()
    
    if request.method == "POST":
        check = request.form.get("check")
        if check == "True":
            check = True
        else:
            check = False

    if reg_form.validate():

        inp_email = reg_form.email.data
        inp_nick = reg_form.username.data
        inp_password = reg_form.password.data
        
        obj_user = Users.query.filter_by(username=inp_nick).first()
        if obj_user:
            return redirect(url_for("user.view_register"))

        if len(inp_nick)>2:
            nick = inp_nick

            if len(inp_password)>7:
                password = inp_password

                new_user = Users(username = nick, email = inp_email, subscribe=check)
                new_user.set_password(password)

                db.session.add(new_user)
                db.session.commit()

                session["logged"] = nick

                return redirect(url_for("article.view_home"))

            else:
                return render_template("User/register.html", form=reg_form)

    return redirect(url_for("user.view_register"))

@user.route("/change_password/", methods=["GET"])
def view_change_password():
    if "logged" not in session:
        return redirect(url_for("view_login"))

    form = ChangePassword()
    return render_template("User/change_password.html", form=form)

@user.route("/change_password/", methods=["POST"])
def change_password():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    
    form = ChangePassword()
    if form.validate():
        user = Users.query.filter_by(username = session["logged"]).first()
        if user and user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for("article.view_home"))    
        else:
            return render_template("User/change_password.html", form=form)
    else:
        return render_template("User/change_password.html", form=form)

@user.route("/logout/", methods=["POST"])
def logout():
    session.pop("logged")
    return redirect(url_for("article.view_home"))