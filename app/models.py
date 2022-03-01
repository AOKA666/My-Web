from app import db,app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login
from datetime import datetime
from flask import current_app
from time import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Permission:
    COMMENT = 1
    WRITE = 2
    

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
    )
    
    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    real_avatar = db.Column(db.String(128), default=None)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),lazy='dynamic'
    )
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
        
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
            
    def followed_comments(self):
        followed = Comments.query.join(
            followers, (followers.c.followed_id == Comments.author_id)).filter(
                followers.c.follower_id == self.id)
        own = Comments.query.filter_by(author_id=self.id)
        return followed.union(own).order_by(Comments.timestamp.desc())
        
    def get_reset_password_token(self, expires_in=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in)
        return s.dumps({'reset_password': self.id}).decode('utf-8')
            
    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return
        return User.query.get(data['reset_password'])


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comments', backref='post', lazy='dynamic')
    
    def __repr__(self):
        return '<Post %s>' % self.title


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    #若不存在，默认self.permission=0，下方self.has_permission要用到
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.COMMENT],
            'Admin': [Permission.COMMENT, Permission.WRITE]
        }
        default_role = 'User'
        for r in roles:
            # 第一步查询，是因为首次进来会直接运行role=Role(name=r)
            # 而name是唯一的，第二次无法再创建，只能查询出原有的进行赋值
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permissions(perm)
            # role.default判断是否是默认角色，即是不是“用户”，不知道干嘛用的
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()
            
    def add_permissions(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
            
    def remove_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions -= perm
        
    def reset_permissions(self):
        self.permissions = 0
        
    # &位运算，有0为0，全1为1
    # 从左往右计算，看self.permissions & perm和perm是否相等
    # 由于全是1,2,4等数字，位运算有奇效
    def has_permission(self, perm):
        return self.permissions & perm == perm
        
    def __repr__(self):
        return '<Role %r>' % self.name


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

login.anonymous_user = AnonymousUser


class Comments(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    
    def __repr__(self):
        return '<Comment %s>' % self.body