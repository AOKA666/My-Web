from flask import Flask, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_bootstrap import Bootstrap
from app import db, ckeditor
from app.main import bp
from .forms import EditForm
from ..auth.forms import CommentForm
from ..models import User, Post, Permission, Comments
import os, datetime, random
import json
from flask_ckeditor import upload_success, upload_fail
import math
from datetime import datetime


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET','POST'])
def index():
    f = open("app/templates/dwyw.txt")
    dwyw = [line.strip('\n') for line in f.readlines()]
    f2 = open("app/templates/rmzx.txt")
    rmzx = f2.readlines()
    f3 = open("app/templates/blbl.txt")
    blbl = f3.readlines()
    return render_template("index.html", dwyw=dwyw, rmzx=rmzx, blbl=blbl)


@bp.route('/animals/<area>/<page>')
def show(area, page):
    if area == 'land':
        f = open("app/templates/land_animal_list.txt")
        title = '陆地动物'
        name = 'land_animal'
        location = 'land'
    elif area == 'sky':
        f = open("app/templates/sky_animal_list.txt")
        title = '天空动物'
        name = 'sky_animal'
        location = 'sky'
    elif area == 'ocean':
        f = open("app/templates/ocean_animal_list.txt")
        title = '海洋动物'
        name = 'ocean_animal'
        location = 'ocean'
    animal = [line.strip('\n') for line in f.readlines()]
    num = len(animal)
    en_name = [i.split()[0] for i in animal]
    ch_name = [i.split()[1] for i in animal]
    description = [i.split()[2] for i in animal]
    result = []
    result.append(en_name)
    result.append(ch_name)
    result.append(description)
    perpage = current_app.config['IMAGE_PER_PAGE']
    start= (int(page)-1) * perpage
    end = int(page) * perpage
    if end > num:
        end = num
    end_page = math.ceil(num/perpage)
    return render_template("animals.html", title=title, name=name, location=location, result=result, start=start, end=end, 
                            perpage=perpage, end_page=end_page)


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@bp.route('/upload', methods=['Post'])
def upload():
    error = ''
    if request.method == 'POST' and 'upload' in request.files:
        f = request.files.get('upload')
        extension = f.filename.split('.')[-1].lower()
        if extension not in ['jpg', 'gif', 'png', 'jpeg']:
            return upload_fail(message='Image only!')
        fname, fext = os.path.splitext(f.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)        
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
                return upload_fail(message=error)
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
            return upload_fail(message =error)
        if not error:
            f.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
            return upload_success(url=url)
    else:
        return upload_fail(message='Post Error!')


@bp.route('/article/<title>/delete/<id>', methods=['GET','POST'])
def delete(title, id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.article', title=title))


@bp.route('/article/<title>', methods=['GET','POST'])
def article(title):
    form = EditForm()
    form2 = CommentForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('提交成功')
        return redirect(url_for('main.article', title=form.title.data))
    posts = Post.query.filter_by(title=title).first()
    if form2.validate_on_submit():
        comment = Comments(body=form2.body.data,post_id=posts.id,author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.article', title=title))
    # 评论分页
    page = request.args.get('page',1,type=int)
    if posts:
        comments = Comments.query.filter_by(post_id=posts.id).order_by(Comments.timestamp.desc()).paginate(
            page, current_app.config['COMMENTS_PER_PAGE'], False)
        next_url = url_for('main.article', title=title, page=comments.next_num)\
            if comments.has_next else None
        prev_url = url_for('main.article', title=title, page=comments.prev_num) \
            if comments.has_prev else None
    else:
        comments = {}
        next_url = ''
        prev_url = ''
    return render_template("article.html", title=title, form=form, form2=form2, 
                            posts=posts, comments=comments.items, next_url=next_url, prev_url=prev_url, Permission=Permission)
 

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    comments = Comments.query.filter_by(author_id=user.id).all()
    return render_template('user.html', user=user, comments=comments)
    

@bp.route('/article/<title>/edit/<id>', methods=['GET','POST'])
def edit(title, id):
    content = Post.query.get(id)
    form = EditForm(title=content.title, body=content.body)
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.delete(content)
        db.session.commit()
        db.session.add(post)
        db.session.commit()
        flash('编辑成功')
        return redirect(url_for('main.article', title=form.title.data))
    posts = Post.query.filter_by(title=title).all()
    return render_template("article.html", title=title, form=form, posts=posts, Permission=Permission)
