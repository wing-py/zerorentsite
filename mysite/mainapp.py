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
@app.route('/submit_order')
def submit_order():
    return render_template('submit_order.html')

# 浏览订单
@app.route('/list_order')
def list_order():
    return render_template('list_order.html')

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