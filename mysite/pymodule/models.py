from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# 创建数据库实例
db = SQLAlchemy()

# 导入模型
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 身份标记字段
    is_devlop = db.Column(db.Boolean, default=False)
    is_custom = db.Column(db.Boolean, default=False)

    # 开发者信息字段
    dev_skills = db.Column(db.JSON, nullable=True) # 存储技能列表，使用JSON格式
    description = db.Column(db.Text, nullable=True) # 描述
    note = db.Column(db.Text, nullable=True) # 备注

    # 个人信息字段
    real_name = db.Column(db.String(50))
    id_card = db.Column(db.String(18))
    qq = db.Column(db.String(20))
    wechat = db.Column(db.String(50))
    github = db.Column(db.String(100)) # 添加 GitHub 用户名字段

    # 第三方登录字段
    wechat_openid = db.Column(db.String(100))
    qq_openid = db.Column(db.String(100))
    github_id = db.Column(db.String(100), unique=True, nullable=True) # 添加 GitHub ID 字段

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

# Project Model
class Project(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) # 数据项id
    who = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False) # 参与人id
    job = db.Column(db.String(200)) # 参与工作
    url = db.Column(db.String(200)) # 项目链接
    name = db.Column(db.String(200)) # 项目名称
    text = db.Column(db.String(200)) # 项目介绍文件路径

    # Establish relationship with User
    developer = db.relationship('User', backref='projects')
