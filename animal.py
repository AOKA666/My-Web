from app import app
from app.models import db, User, Post, Role

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post, 'Role': Role}
