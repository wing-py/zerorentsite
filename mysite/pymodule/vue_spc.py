import os
from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session, jsonify,send_from_directory

vue_spc_bp = Blueprint('vue_spc', __name__)

# 显式处理 assets 资源请求
@vue_spc_bp.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('vue-build/assets', filename)

# 首页
@vue_spc_bp.route('/')
def index():
    # return render_template('index.html')
    return send_from_directory('vue-build','index.html')

@vue_spc_bp.route('/<path:path>')
def static_files(path):
    if path and os.path.exists(os.path.join('vue-build', path)):
        return send_from_directory('vue-build', path)
    return send_from_directory('vue-build','index.html')
