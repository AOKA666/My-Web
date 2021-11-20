from flask import Flask, render_template, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from flask_bootstrap import Bootstrap
from app import app
from .forms import LoginForm
from .models import User


@app.route('/', methods=['GET','POST'])
def index():
    f = open("app/templates/dwyw.txt")
    dwyw = f.readlines()
    f2 = open("app/templates/rmzx.txt")
    rmzx = f2.readlines()
    f3 = open("app/templates/blbl.txt")
    blbl = f3.readlines()
    return render_template("index.html", dwyw=dwyw, rmzx=rmzx, blbl=blbl)

@app.route('/land')
def show():
    return render_template("land.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('登录成功')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
