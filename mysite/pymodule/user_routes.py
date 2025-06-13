from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from .models import db, Order, User, Comment, Project

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

    # 获取项目数据
    project_job = request.form.get('project_job')
    project_url = request.form.get('project_url')
    project_name = request.form.get('project_name')
    project_text = request.form.get('project_text')

    # 如果有项目数据，则创建新项目并关联到用户
    if project_job or project_url or project_name or project_text:
        new_project = Project(
            who=user.id,
            job=project_job,
            url=project_url,
            name=project_name,
            text=project_text
        )
        db.session.add(new_project)

    try:
        db.session.commit()
        flash('开发者简历和项目信息更新成功', 'success')
        return redirect(url_for('user.profile'))
    except Exception as e:
        db.session.rollback()
        flash(f'更新开发者简历和项目信息失败: {str(e)}', 'danger')
        return redirect(url_for('user.profile'))

# 查看某用户详情
@user_bp.route('/view_user/<string:user_id>')
def view_user(user_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('请先登录才能查看开发者简历', 'warning')
        return redirect(url_for('auth.login'))
    
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

    # Fetch user's projects
    user_projects = Project.query.filter_by(who=user.id).all()
    # Convert projects to a list of dictionaries for JSON serialization
    projects_data = []
    for project in user_projects:
        project_data = {}
        for column in project.__table__.columns:
            project_data[column.name] = getattr(project, column.name)
        projects_data.append(project_data)


    return render_template('view_user.html', user=user, user_data=user_data, projects=projects_data)

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

    # Fetch user's projects
    user_projects = Project.query.filter_by(who=user.id).all()
    # Convert projects to a list of dictionaries for JSON serialization
    projects_data = []
    for project in user_projects:
        project_data = {}
        for column in project.__table__.columns:
            project_data[column.name] = getattr(project, column.name)
        projects_data.append(project_data)


    return render_template('profile.html', user=user, user_data=user_data, projects=projects_data)

# 添加新项目
@user_bp.route('/add_project', methods=['POST'])
def add_project():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': '用户未登录'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    data = request.get_json()
    name = data.get('name')
    job = data.get('job')
    url = data.get('url')
    text = data.get('text')

    if not name:
        return jsonify({'success': False, 'message': '项目名称不能为空'}), 400

    new_project = Project(
        who=user.id,
        name=name,
        job=job,
        url=url,
        text=text
    )

    try:
        db.session.add(new_project)
        db.session.commit()
        return jsonify({'success': True, 'message': '项目添加成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'项目添加失败: {str(e)}'}), 500

# 编辑项目
@user_bp.route('/edit_project', methods=['POST'])
def edit_project():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': '用户未登录'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    data = request.get_json()
    project_id = data.get('id')
    name = data.get('name')
    job = data.get('job')
    url = data.get('url')
    text = data.get('text')

    if not project_id:
        return jsonify({'success': False, 'message': '项目ID不能为空'}), 400

    project = Project.query.filter_by(id=project_id, who=user.id).first()
    if not project:
        return jsonify({'success': False, 'message': '项目不存在或无权编辑'}), 404

    project.name = name
    project.job = job
    project.url = url
    project.text = text

    try:
        db.session.commit()
        return jsonify({'success': True, 'message': '项目更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'项目更新失败: {str(e)}'}), 500

# 删除项目
@user_bp.route('/delete_project', methods=['POST'])
def delete_project():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': '用户未登录'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    data = request.get_json()
    project_id = data.get('project_id')

    if not project_id:
        return jsonify({'success': False, 'message': '项目ID不能为空'}), 400

    project = Project.query.filter_by(id=project_id, who=user.id).first()
    if not project:
        return jsonify({'success': False, 'message': '项目不存在或无权删除'}), 404

    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'success': True, 'message': '项目删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'项目删除失败: {str(e)}'}), 500
