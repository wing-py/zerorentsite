# 第三方注册模块
from flask import Flask
import os
from flask_cors import CORS


# 项目自维护模块
from pymodule.models import db
from pymodule.main_routes import main_bp
from pymodule.auth_routes import auth_bp
from pymodule.user_routes import user_bp
from pymodule.order_routes import order_bp
from pymodule.forum_routes import forum_bp
from pymodule.vue_spc import vue_spc_bp
from pymodule.apis import apis_bp



app = Flask(__name__)
# CORS(app)
CORS(app,
     resources={r"/\*": {"origins": "\*"}},  # 允许所有源访问所有路由
     supports_credentials=True,            # 允许携带 Cookie
     methods=["GET", "POST", "PUT", "DELETE"],  # 允许的请求方法
     allow_headers=["Content-Type", "Authorization"]  # 允许的请求头
)
app.config.from_pyfile('config.py')

# 初始化数据库到应用
db.init_app(app)

# 使用static+templates
# 注册蓝图
# app.register_blueprint(main_bp)
# app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(user_bp)
# app.register_blueprint(order_bp)
# app.register_blueprint(forum_bp)

# 使用vue-build
app.register_blueprint(apis_bp)
app.register_blueprint(vue_spc_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)