from app.page import bp
from flask import render_template


@bp.route('/hotsection/tiger')
def hotsection_tiger():
    return render_template('hot_section/tiger.html')
    
@bp.route('/hotsection/tiger/machili')
def machili():
    return render_template('hot_section/machili.html')
    
@bp.route('/hot_section/lion')
def hotsection_lion():
    return render_template('hot_section/lion.html')