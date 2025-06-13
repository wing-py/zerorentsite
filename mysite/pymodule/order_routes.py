from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from .models import db, Order, User, Comment

order_bp = Blueprint('order', __name__)

# 发布订单
@order_bp.route('/submit_order', methods=['GET', 'POST'])
def submit_order():
    if not session.get('user_id'):
        flash('请先登录才能发布订单')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Handle form submission
        if not session.get('user_id'):
            flash('请先登录才能发布订单')
            return redirect(url_for('auth.login'))

        category = request.form.get('category')
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        period = request.form.get('period')
        contact_type = request.form.get('contact_type')
        contact_value = request.form.get('contact_value')
        contact = contact_type + contact_value

        # Basic validation
        if not all([category, title, description, price, period, contact]):
            flash('所有字段都是必填项')
            return redirect(url_for('order.submit_order'))

        try:
            price = float(price)
        except ValueError:
            flash('佣金必须是有效的数字')
            return redirect(url_for('order.submit_order'))

        user_id = session['user_id']
        new_order = Order(
            category=category,
            title=title,
            description=description,
            price=price,
            period=period,
            contact=contact,
            submiter_id=user_id
        )

        db.session.add(new_order)
        db.session.commit()

        flash('订单发布成功！')
        return redirect(url_for('order.list_order')) # Redirect to the order list page

    # For GET request, render the form
    return render_template('submit_order.html')

# 浏览订单
@order_bp.route('/list_order')
def list_order():
    category_filter = request.args.get('category')
    submiter_filter = request.args.get('submiter')

    orders = Order.query

    if category_filter:
        orders = orders.filter_by(category=category_filter)

    if submiter_filter:
        # Assuming submiter_filter is the username
        submiter_user = User.query.filter_by(username=submiter_filter).first()
        if submiter_user:
            orders = orders.filter_by(submiter=submiter_user)
        else:
            flash(f'未找到用户: {submiter_filter}')


    orders = orders.all() # Execute the query

    # Get unique categories and submitters for filters
    categories = [order.category for order in Order.query.distinct(Order.category)]
    submiters = [order.submiter.username for order in Order.query.distinct(Order.submiter_id)]


    return render_template('list_order.html', orders=orders, selected_category=category_filter, selected_submiter=submiter_filter, categories=categories, submiters=submiters) # Pass filters and options to template

# 查看订单详情
@order_bp.route('/order/<order_id>')
def view_order(order_id):
    order = Order.query.get_or_404(order_id) # Fetch the order or return 404
    return render_template('order_detail.html', order=order) # Render the detail template

# 添加评论
@order_bp.route('/order/<order_id>/comment', methods=['POST'])
def add_comment(order_id):
    if not session.get('user_id'):
        flash('请先登录才能评论')
        return redirect(url_for('auth.login'))

    order = Order.query.get_or_404(order_id)
    comment_content = request.form.get('comment_content')

    if not comment_content:
        flash('评论内容不能为空')
        return redirect(url_for('order.view_order', order_id=order.id))

    user_id = session['user_id']
    new_comment = Comment(
        order_id=order.id,
        who_comment_id=user_id,
        what_comment=comment_content
    )

    db.session.add(new_comment)
    db.session.commit()

    flash('评论添加成功！')
    return redirect(url_for('order.view_order', order_id=order.id))

# 删除订单
@order_bp.route('/order/<order_id>/delete', methods=['POST'])
def delete_order(order_id):
    if not session.get('user_id'):
        flash('请先登录才能删除订单')
        return redirect(url_for('auth.login'))

    order = Order.query.get_or_404(order_id)

    # Check if the current user is the submiter
    if session['user_id'] != order.submiter_id:
        flash('您无权删除此订单')
        return redirect(url_for('order.view_order', order_id=order.id))

    db.session.delete(order)
    db.session.commit()

    flash('订单删除成功！')
    return redirect(url_for('order.list_order'))

# 修改订单
@order_bp.route('/order/<order_id>/edit', methods=['GET', 'POST'])
def edit_order(order_id):
    if not session.get('user_id'):
        flash('请先登录才能修改订单')
        return redirect(url_for('auth.login'))

    order = Order.query.get_or_404(order_id)

    # Check if the current user is the submiter
    if session['user_id'] != order.submiter_id:
        flash('您无权修改此订单')
        return redirect(url_for('order.view_order', order_id=order.id))

    if request.method == 'POST':
        # Handle form submission for editing
        order.category = request.form.get('category')
        order.title = request.form.get('title')
        order.description = request.form.get('description')
        order.price = request.form.get('price')
        order.contact = request.form.get('contact')
        order.period = request.form.get('period')

        # Basic validation (similar to submit_order)
        if not all([order.category, order.title, order.description, order.price, order.contact, order.period]):
            flash('所有字段都是必填项')
            return redirect(url_for('order.edit_order', order_id=order.id))

        try:
            order.price = float(order.price)
        except ValueError:
            flash('佣金必须是有效的数字')
            return redirect(url_for('order.edit_order', order_id=order.id))

        db.session.commit()

        flash('订单修改成功！')
        return redirect(url_for('order.view_order', order_id=order.id)) # Redirect to the order detail page

    # For GET request, render the edit form
    return render_template('edit_order.html', order=order)
