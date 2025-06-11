import os

# Flask配置
SECRET_KEY = os.urandom(24)
DEBUG = True

# 数据库配置
SQLALCHEMY_DATABASE_URI = 'sqlite:///rider_mailbox.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 文件上传配置
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/images/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 创建上传文件夹
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# GitHub OAuth 配置
GITHUB_CLIENT_ID = 'Ov23liUEx0dyBdpjAduS'
GITHUB_CLIENT_SECRET = 'a66d3f827754dde4317f168e50b1c0b2ad0aeeb1'
GITHUB_CALLBACK_URL = 'http://127.0.0.1:5000/auth/login/github/callback' # 请根据你的应用配置修改