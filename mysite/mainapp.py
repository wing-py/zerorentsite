# 第三方注册模块
from flask import Flask
import os

# 项目自维护模块
from pymodule.models import db
from pymodule.main_routes import main_bp
from pymodule.auth_routes import auth_bp
from pymodule.user_routes import user_bp
from pymodule.order_routes import order_bp
from pymodule.forum_routes import forum_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

# 初始化数据库到应用
db.init_app(app)

# 注册蓝图
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp)
app.register_blueprint(order_bp)
app.register_blueprint(forum_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)