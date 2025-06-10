from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from .models import db, User

auth_bp = Blueprint('auth', __name__)

# 注册
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return redirect(url_for('auth.register'))

        # 验证新密码是否匹配
        if password != confirm_password:
            flash('新密码和确认密码不一致')
            return redirect(url_for('auth.register'))

        # 创建新用户
        new_user = User(
            id=str(uuid.uuid4()),
            username=username,
            password=generate_password_hash(password),
            email=email,
            phone=phone
        )

        db.session.add(new_user)
        db.session.commit()

        flash('注册成功，请登录')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# 登录
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main.index'))
        else:
            flash('用户名或密码错误')

    return render_template('login.html')

# 注销
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))

# 个人信息页面
@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user_id'):
        flash('请先登录')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        # 更新用户信息
        user.username = request.form.get('username')
        user.real_name = request.form.get('real_name')
        user.id_card = request.form.get('id_card')
        user.phone = request.form.get('phone')
        user.qq = request.form.get('qq')
        user.wechat = request.form.get('wechat')
        user.email = request.form.get('email')

        db.session.commit()

        flash('个人信息已更新')
        return redirect(url_for('auth.profile'))
    
    # Dynamically create a dictionary from user object columns
    user_data = {}
    for column in user.__table__.columns:
        # Exclude sensitive fields like password
        if column.name != 'password':
             user_data[column.name] = getattr(user, column.name)

    return render_template('profile.html', user=user, user_data=user_data)

# 更改密码页面
@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if not session.get('user_id'):
        flash('请先登录')
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # 验证旧密码
        if not check_password_hash(user.password, old_password):
            flash('旧密码不正确')
            return redirect(url_for('auth.change_password'))

        # 验证新密码是否匹配
        if new_password != confirm_password:
            flash('新密码和确认密码不一致')
            return redirect(url_for('auth.change_password'))

        # 更新密码
        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash('密码已成功更新')
        return redirect(url_for('auth.profile'))

    return render_template('change_password.html')

# 检查用户名是否已存在
@auth_bp.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': '缺少用户名'}), 400

    user = User.query.filter_by(username=username).first()

    return jsonify({'available': user is None})
