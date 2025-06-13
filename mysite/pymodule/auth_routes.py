from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
import requests
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
        callname = request.form.get('callname') # 获取称呼名
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
            callname=callname if callname else username, # 如果称呼名为空，使用账号名
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

# 解绑 GitHub 账号
@auth_bp.route('/unbind_github', methods=['POST'])
def unbind_github():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    data = request.get_json()
    password = data.get('password')

    # 验证密码
    if not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': '密码不正确。如果您不知道密码，请使用忘记密码功能重置。'}), 400

    if user.github_id:
        user.github_id = None
        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'GitHub 账号已成功解绑'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'解绑失败: {str(e)}'}), 500
    else:
        return jsonify({'success': False, 'message': '当前账号未绑定 GitHub'}), 400

# GitHub 登录
@auth_bp.route('/login/github')
def github_login():
    github_auth_url = 'https://github.com/login/oauth/authorize'
    params = {
        'client_id': current_app.config['GITHUB_CLIENT_ID'],
        'redirect_uri': current_app.config['GITHUB_CALLBACK_URL'],
        'scope': 'user:email' # 请求用户邮箱权限
    }
    return redirect(f'{github_auth_url}?{"&".join([f"{k}={v}" for k, v in params.items()])}')

# GitHub 回调处理
@auth_bp.route('/login/github/callback')
def github_callback():
    code = request.args.get('code')
    if not code:
        flash('GitHub 认证失败', 'danger')
        return redirect(url_for('auth.login'))

    # 交换授权码获取访问令牌
    token_url = 'https://github.com/login/oauth/access_token'
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': current_app.config['GITHUB_CLIENT_ID'],
        'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
        'code': code,
        'redirect_uri': current_app.config['GITHUB_CALLBACK_URL']
    }
    response = requests.post(token_url, headers=headers, json=data)
    token_info = response.json()

    if 'access_token' not in token_info:
        flash('获取 GitHub 访问令牌失败', 'danger')
        return redirect(url_for('auth.login'))

    access_token = token_info['access_token']

    # 使用访问令牌获取用户信息
    user_info_url = 'https://api.github.com/user'
    headers = {'Authorization': f'token {access_token}'}
    user_response = requests.get(user_info_url, headers=headers)
    github_user_info = user_response.json()

    github_id = str(github_user_info.get('id'))
    github_username = github_user_info.get('login')
    github_email = github_user_info.get('email') # 可能需要额外请求权限或用户设置公开邮箱

    # 查找用户
    user = User.query.filter_by(github_id=github_id).first()

    if user:
        # 用户已存在，直接登录
        session['user_id'] = user.id
        session['username'] = user.username
        flash('使用 GitHub 登录成功', 'success')
        return redirect(url_for('main.index'))
    else:
        # 新用户或需要绑定
        if session.get('user_id'):
            # 用户已登录，进行绑定
            current_user = User.query.get(session['user_id'])
            if current_user.github_id:
                flash('当前账号已绑定其他 GitHub 账号', 'warning')
            else:
                current_user.github_id = github_id
                current_user.github = github_username # 保存 GitHub 用户名
                # 可以选择更新其他信息，例如邮箱
                if not current_user.email and github_email:
                    current_user.email = github_email
                db.session.commit()
                flash('GitHub 账号绑定成功', 'success')
            return redirect(url_for('user.profile')) # 重定向到个人信息页面

        else:
            # 新用户，创建账号
            # 检查用户名是否已存在（如果 GitHub 用户名与现有用户名冲突）
            existing_user = User.query.filter_by(username=github_username).first()
            if existing_user:
                # 用户名冲突，可以提示用户手动绑定或选择其他方式
                flash(f'GitHub 用户名 "{github_username}" 已存在，请尝试绑定现有账号或使用其他方式登录/注册', 'warning')
                return redirect(url_for('auth.login'))

            new_user = User(
                id=str(uuid.uuid4()),
                username=github_username,
                github_id=github_id,
                github=github_username, # 保存 GitHub 用户名
                email=github_email,
                # 可以根据需要设置其他默认值
            )
            # GitHub 登录不需要密码，但模型中 password 是 nullable=False，需要处理
            # 可以在模型中设置 password 为 nullable=True，或者为 GitHub 登录的用户生成一个随机密码
            # 这里选择生成随机密码
            new_user.password = generate_password_hash(str(uuid.uuid4())) # 生成随机密码

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            session['username'] = new_user.username
            flash('使用 GitHub 注册并登录成功', 'success')
            return redirect(url_for('main.index'))

# 个人信息页面(已废弃，profile功能迁移到user模块)
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
        return redirect(url_for('user.profile'))
    
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

        # 验证新密码是否匹配
        if new_password != confirm_password:
            flash('新密码和确认密码不一致')
            return redirect(url_for('auth.change_password'))

        # 更新密码
        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash('密码已成功更新')
        return redirect(url_for('user.profile'))

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
