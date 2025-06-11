from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from .models import db, Order, User, Comment

user_bp = Blueprint('user', __name__)

# 寻找开发者
@user_bp.route('/list_worker')
def list_worker():
    user_count = User.query.count()
    users = User.query.order_by(User.created_at).all()
    users_data = []
    for user in users:
        user_data = {}
        for column in user.__table__.columns:
            # Exclude sensitive fields like password
            if column.name not in ['password']:
                 user_data[column.name] = getattr(user, column.name)
        users_data.append(user_data)
    return render_template('list_worker.html', user_count=user_count, users=users, users_data=users_data)

# 用户更换身份
@user_bp.route('/toggle_identity', methods=['POST'])
def toggle_identity():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': '用户未登录'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    data = request.get_json()
    identity_type = data.get('identity_type')
    state = data.get('state')

    if identity_type == 'developer':
        user.is_devlop = state
    elif identity_type == 'customer':
        user.is_custom = state
    else:
        return jsonify({'success': False, 'message': '无效的身份类型'}), 400

    try:
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': '身份标记更新成功', 
            'identify_type': identity_type,
            'state':state
                        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'更新失败: {str(e)}'}), 500

# 用户编辑开发简历
@user_bp.route('/edit_developer_profile', methods=['POST'])
def edit_developer_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('请先登录才能编辑开发者简历', 'warning')
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('main.index')) # 或者重定向到其他合适的页面

    # 获取表单数据
    dev_skills_str = request.form.get('dev_skills')
    description = request.form.get('description')
    note = request.form.get('note')

    # 将技能字符串转换为列表（如果需要的话，这里简单处理为字符串）
    # TODO: 更复杂的技能处理，例如JSON格式
    user.dev_skills = dev_skills_str # 暂时存储为字符串，后续可以改为JSON
    user.description = description
    user.note = note

    try:
        db.session.commit()
        flash('开发者简历更新成功', 'success')
        return redirect(url_for('user.profile'))
    except Exception as e:
        db.session.rollback()
        flash(f'更新开发者简历失败: {str(e)}', 'danger')
        return redirect(url_for('user.profile'))

# 查看某用户详情
@user_bp.route('/viewuser/<string:user_id>')
def viewuser(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('main.index'))

    # Dynamically create a dictionary from user object columns
    user_data = {}
    for column in user.__table__.columns:
        # Exclude sensitive fields like password
        if column.name != 'password':
             user_data[column.name] = getattr(user, column.name)

    return render_template('profile.html', user=user_data) # Pass the dictionary

# 个人信息页面
@user_bp.route('/profile', methods=['GET', 'POST'])
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
