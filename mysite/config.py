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