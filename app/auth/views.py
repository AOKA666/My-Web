from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_bootstrap import Bootstrap
from app import db, ckeditor
from app.auth import bp
from .forms import LoginForm, RegistrationForm, CommentForm, ChangeAvatarForm, EditProfileForm
from ..models import User, Post, Permission, Comments
import os, datetime, random
import json
from flask_ckeditor import upload_success, upload_fail
import math
from datetime import datetime
from ..email import send_password_reset_email
from .forms import ResetPasswordRequestForm, ResetPasswordForm


@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash('登录成功')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)
 
 
@bp.route('/logout')
def logout():
    logout_user()
    flash('您已登出')
    return redirect(url_for('main.index'))
    
    
@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('registraion success!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)    
 
 
@bp.route('/user/change-avatar', methods=['GET','POST'])
@login_required
def change_avatar():
    form = ChangeAvatarForm()
    if form.validate_on_submit():
        avatar = request.files['avatar']
        fname = avatar.filename
        # 存储路径
        upload_folder = current_app.config['UPLOAD_FOLDER']
        allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
        fext = fname.rsplit('.',1)[-1] if '.' in fname else ''
        # 判断是否符合要求
        if fext not in allowed_extensions:
            flash('文件格式错误！')
            return redirect(url_for('main.user', username=current_user.username))
        # 存储文件的文件名
        target = '{}{}.{}'.format(upload_folder, current_user.username, fext)
        avatar.save(target)
        current_user.real_avatar = '/static/avatars/{}.{}'.format(current_user.username, fext)
        db.session.commit()
        flash('用户头像已更新')
        return redirect(url_for('user', username=current_user.username))
    return render_template('change_avatar.html', form=form)
 
 
@bp.route('/user/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('信息编辑成功！')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='编辑信息',form=form)
 
 
@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('未找到用户 {}'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('不能关注自己!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('你已关注 {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('未找到用户 {}'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('不能取关你自己！')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('你已取关 {}'.format(username))
    return redirect(url_for('main.user', username=username))
    
    
@bp.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('重置密码链接已发送，请检查邮箱！')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                            title='重置密码',form=form)


@bp.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('密码重置成功！')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
    
@bp.route('/article/<title>/deleteComments/<id>', methods=['GET','POST'])
def deleteComments(title, id):
    comment = Comments.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论删除成功！')
    return redirect(url_for('main.article', title=title))