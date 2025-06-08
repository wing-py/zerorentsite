from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
forum_static_path = os.path.join(here,'static','forum')

app = Flask(__name__)
app.config.from_pyfile('config.py')

# 初始化数据库
db = SQLAlchemy(app)

# 导入模型
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 个人信息字段
    real_name = db.Column(db.String(50))
    id_card = db.Column(db.String(18))
    qq = db.Column(db.String(20))
    wechat = db.Column(db.String(50))

    # 第三方登录字段
    wechat_openid = db.Column(db.String(100))
    qq_openid = db.Column(db.String(100))

    # 关联信函
    letters = db.relationship('Letter', backref='author', lazy=True)

class Letter(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    display_permission = db.Column(db.String(20), default='希望展示')
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 外键关联用户
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)

# Order Model
class Order(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # id 订单号
    category = db.Column(db.String(100)) # class 类目
    title = db.Column(db.String(200)) # title 标题
    description = db.Column(db.Text) # description 描述
    price = db.Column(db.Numeric(10, 2)) # price 佣金
    contact = db.Column(db.String(200)) # contact 联系
    period = db.Column(db.String(100), nullable=True) # period 工期
    when_submitted = db.Column(db.DateTime, default=datetime.now) # when 发布时间
    submiter_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False) # who 发布用户
    submiter = db.relationship('User', backref='submitted_orders')

    discuss_id = db.Column(db.Integer, nullable=True) # discuss_id 讨论号
    contract = db.Column(db.Text, nullable=True) # contract 合同

    # Many-to-Many relationship for undertakers
    undertakers = db.relationship('User', secondary='order_undertakers', backref='undertaken_orders')

    developer_evaluate_to_submiter = db.Column(db.Text, nullable=True) # developer_evaluate_to_submiter
    submiter_evaluate_to_developer = db.Column(db.Text, nullable=True) # submiter_evaluate_to_developer

# Association table for Many-to-Many relationship
order_undertakers = db.Table('order_undertakers',
    db.Column('order_id', db.String(36), db.ForeignKey('order.id'), primary_key=True),
    db.Column('user_id', db.String(36), db.ForeignKey('user.id'), primary_key=True)
)


# Comment Model
class Comment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('order.id'), nullable=False) # Link to the Order
    order = db.relationship('Order', backref='comments')
    who_comment_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False) # who_comment 表达人
    who_comment = db.relationship('User', backref='order_comments')
    what_comment = db.Column(db.Text) # what_comment 意见陈述
    comment_time = db.Column(db.DateTime, default=datetime.now) # When the comment was made

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 介绍
@app.route('/about')
def about():
    return render_template('about.html')

# 论坛
## 论坛主页
@app.route('/forum')
def forum():
    topics = os.listdir(forum_static_path)
    return render_template('forum.html', topics=topics)

## 论坛话题
@app.route('/forum/topic/<topic_name>', methods=['GET', 'POST'])
def forum_topic(topic_name):
    # 获取话题的所有文件
    topic_path = os.path.join(forum_static_path, topic_name)
    if not os.path.exists(topic_path):
        flash('话题不存在')
        return redirect(url_for('forum'))
    if request.method == 'POST':
            # 处理用户提交的内容
            #username = request.form.get('username') # 从表单获取用户名
            if not session.get('user_id'):
                flash('请先登录')
                return redirect(url_for('login'))
            username = session.get('username')  # 从会话获取用户名
            content = request.form.get('content')

            if username and content:
                file_path = os.path.join(topic_path, username + '.txt')
                with open(file_path, 'w') as f:
                    f.write(content)
                return redirect(url_for('forum_topic', topic_name=topic_name))
    # 获取该话题下的所有用户评论
    comments = []
    if os.path.exists(topic_path):
        for filename in os.listdir(topic_path):
            if filename.endswith('.txt'):
                username = filename[:-4]  # 去掉 .txt 扩展名
                with open(os.path.join(topic_path, filename), 'r') as f:
                    content = f.read()
                comments.append({'username': username, 'content': content})

    return render_template('topic.html', topic_name=topic_name, comments=comments)


# 发布订单
@app.route('/submit_order', methods=['GET', 'POST'])
def submit_order():
    if request.method == 'POST':
        # Handle form submission
        if not session.get('user_id'):
            flash('请先登录才能发布订单')
            return redirect(url_for('login'))

        category = request.form.get('category')
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        contact = request.form.get('contact')

        # Basic validation
        print([category, title, description, price, contact])
        if not all([category, title, description, price, contact]):
            flash('所有字段都是必填项')
            return redirect(url_for('submit_order'))

        try:
            price = float(price)
        except ValueError:
            flash('佣金必须是有效的数字')
            return redirect(url_for('submit_order'))

        user_id = session['user_id']
        new_order = Order(
            category=category,
            title=title,
            description=description,
            price=price,
            contact=contact,
            period=period,
            submiter_id=user_id
        )

        db.session.add(new_order)
        db.session.commit()

        flash('订单发布成功！')
        return redirect(url_for('list_order')) # Redirect to the order list page

    # For GET request, render the form
    return render_template('submit_order.html')

# 浏览订单
@app.route('/list_order')
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
@app.route('/order/<order_id>')
def view_order(order_id):
    order = Order.query.get_or_404(order_id) # Fetch the order or return 404
    return render_template('order_detail.html', order=order) # Render the detail template

# 添加评论
@app.route('/order/<order_id>/comment', methods=['POST'])
def add_comment(order_id):
    if not session.get('user_id'):
        flash('请先登录才能评论')
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)
    comment_content = request.form.get('comment_content')

    if not comment_content:
        flash('评论内容不能为空')
        return redirect(url_for('view_order', order_id=order.id))

    user_id = session['user_id']
    new_comment = Comment(
        order_id=order.id,
        who_comment_id=user_id,
        what_comment=comment_content
    )

    db.session.add(new_comment)
    db.session.commit()

    flash('评论添加成功！')
    return redirect(url_for('view_order', order_id=order.id))

# 删除订单
@app.route('/order/<order_id>/delete', methods=['POST'])
def delete_order(order_id):
    if not session.get('user_id'):
        flash('请先登录才能删除订单')
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)

    # Check if the current user is the submiter
    if session['user_id'] != order.submiter_id:
        flash('您无权删除此订单')
        return redirect(url_for('view_order', order_id=order.id))

    db.session.delete(order)
    db.session.commit()

    flash('订单删除成功！')
    return redirect(url_for('list_order'))

# 修改订单
@app.route('/order/<order_id>/edit', methods=['GET', 'POST'])
def edit_order(order_id):
    if not session.get('user_id'):
        flash('请先登录才能修改订单')
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)

    # Check if the current user is the submiter
    if session['user_id'] != order.submiter_id:
        flash('您无权修改此订单')
        return redirect(url_for('view_order', order_id=order.id))

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
            return redirect(url_for('edit_order', order_id=order.id))

        try:
            order.price = float(order.price)
        except ValueError:
            flash('佣金必须是有效的数字')
            return redirect(url_for('edit_order', order_id=order.id))

        db.session.commit()

        flash('订单修改成功！')
        return redirect(url_for('view_order', order_id=order.id)) # Redirect to the order detail page

    # For GET request, render the edit form
    return render_template('edit_order.html', order=order)

# 寻找开发者
@app.route('/list_worker')
def list_worker():
    users = User.query.all()
    return render_template('list_worker.html', users=users)

# 注册
@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('register'))

        # 验证新密码是否匹配
        if password != confirm_password:
            flash('新密码和确认密码不一致')
            return redirect(url_for('change_password'))

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
        return redirect(url_for('login'))

    return render_template('register.html')

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')

    return render_template('login.html')

# 注销
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# 个人信息页面
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user_id'):
        flash('请先登录')
        return redirect(url_for('login'))

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
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user)

# 更改密码页面
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if not session.get('user_id'):
        flash('请先登录')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # 验证旧密码
        if not check_password_hash(user.password, old_password):
            flash('旧密码不正确')
            return redirect(url_for('change_password'))

        # 验证新密码是否匹配
        if new_password != confirm_password:
            flash('新密码和确认密码不一致')
            return redirect(url_for('change_password'))

        # 更新密码
        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash('密码已成功更新')
        return redirect(url_for('profile'))

    return render_template('change_password.html')


# 信箱
@app.route('/mailbox')
def mailbox():
    # 获取所有信函
    letters = Letter.query.all()
    return render_template('mailbox.html', letters=letters)

# 撰写信函
@app.route('/compose', methods=['GET', 'POST'])
def compose():
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        display_permission = request.form.get('display_permission')

        # 获取用户信息
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None

        # 创建新信函
        new_letter = Letter(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            category=category,
            display_permission=display_permission,
            ip_address=request.remote_addr,
            created_at=datetime.now()
        )

        # 如果用户已登录，关联用户
        if user:
            new_letter.user_id = user.id

        # 保存信函
        db.session.add(new_letter)
        db.session.commit()

        flash('信函已发送')
        return redirect(url_for('mailbox'))

    return render_template('compose.html')

# 查看信函详情
@app.route('/letter/<letter_id>')
def view_letter(letter_id):
    letter = Letter.query.get_or_404(letter_id)
    return render_template('letter_detail.html', letter=letter)

# 搜索信函
@app.route('/search')
def search():
    query = request.args.get('q', '')
    letters = Letter.query.filter(
        (Letter.title.contains(query)) |
        (Letter.content.contains(query)) |
        (Letter.category.contains(query))
    ).all()
    return render_template('search_results.html', letters=letters, query=query)

# 信息公示
@app.route('/disclosure')
def disclosure():
    return render_template('disclosure.html')

# 提供支持
@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/register_rider')
def register_rider():
    return render_template('register_rider.html')

@app.route('/dev_contribution')
def dev_contribution():
    return render_template('dev_contribution.html')

@app.route('/doc_contribution')
def doc_contribution():
    return render_template('doc_contribution.html')

@app.route('/financial_review')
def financial_review():
    return render_template('financial_review.html')

@app.route('/submit_info')
def submit_info():
    return render_template('submit_info.html')

@app.route('/link')
def link():
    return render_template('link.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/contrib_list')
def contrib_list():
    # 读取 CSV 文件
    try:
        df = pd.read_csv(os.path.join(here,'contrilist.csv'))
        # 确保数据按贡献值降序排列
        df = df.sort_values(by='贡献值', ascending=False)
        # 格式化日期和金额
        df['下单日期'] = df['下单日期'].astype(str)
        df['贡献值'] = df['贡献值'].apply(lambda x: f"{x:.2f}")
        # 将 DataFrame 转换为字典列表
        contrib_data = df.to_dict(orient='records')
        return render_template('contrib_list.html', contrib_data=contrib_data)
    except Exception as e:
        return f"Error loading data: {e}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)