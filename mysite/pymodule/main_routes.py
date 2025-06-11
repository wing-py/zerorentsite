from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

# 首页
@main_bp.route('/')
def index():
    return render_template('index.html')

# 介绍
@main_bp.route('/about')
def about():
    return render_template('about.html')

# 进展
@main_bp.route('/progress')
def progress():
    return render_template('progress.html')

# JSON 阅读器
@main_bp.route('/json_reader')
def json_reader():
    return render_template('json_reader.html')