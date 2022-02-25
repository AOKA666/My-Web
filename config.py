import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    ADMIN = '2781936169@qq.com'
    IMAGE_PER_PAGE = 8
    UPLOAD_FOLDER = os.path.join(basedir, "app/static/avatars/")
    
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = '18217099317@163.com'
    MAIL_PASSWORD = 'EAKIZTWQLPIGRVMJ'
    
    COMMENTS_PER_PAGE = 5

    
    @staticmethod
    def init_app(app):
        pass 
        

