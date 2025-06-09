# 登录系统设计文档

## 1. 概述

本文档描述了基于 Flask 实现的用户登录、注册、注销、个人信息管理和密码修改系统的设计。系统使用 SQLAlchemy 作为 ORM，将用户数据存储在 SQLite 数据库中。

项目文件树如下：

```
.
├── .gitignore
├── readme.md
├── requirements.txt
├── design/
│   └── login.md
└── mysite/
    ├── config.py
    ├── mainapp.py
    ├── instance/
    │   └── taro.db
    ├── static/
    │   ├── assets/
    │   ├── css/
    │   └── js/
    └── templates/
        ├── base.html
        ├── change_password.html
        ├── index.html
        ├── login.html
        ├── profile.html
        └── register.html
```

各文件和目录功能说明：

-   `.gitignore`: Git 版本控制忽略文件配置。
-   `readme.md`: 项目说明文档。
-   `requirements.txt`: 项目所需的 Python 依赖库列表。
-   `design/`: 存放设计文档的目录。
    -   `login.md`: 本文档，描述登录系统的设计。
-   `mysite/`: Flask 应用主目录。
    -   `config.py`: Flask 应用的配置信息，如 SECRET_KEY, 数据库 URI 等。
    -   `mainapp.py`: Flask 应用主程序文件，包含路由定义、视图函数和数据库模型。
    -   `instance/`: 存放应用实例相关文件，如 SQLite 数据库文件。
        -   `taro.db`: SQLite 数据库文件，存储用户数据。
    -   `static/`: 存放静态资源的目录。
        -   `assets/`: 存放图片等资源。
        -   `css/`: 存放 CSS 样式文件。
        -   `js/`: 存放 JavaScript 文件。
    -   `templates/`: 存放 HTML 模板文件的目录。
        -   `base.html`: 基础模板文件。
        -   `change_password.html`: 修改密码页面模板。
        -   `index.html`: 首页模板。
        -   `login.html`: 登录页面模板。
        -   `profile.html`: 个人信息页面模板。
        -   `register.html`: 注册页面模板。

## 2. 用户模型 (User Model)

用户模型 [`User`](mysite/mainapp.py:18) 定义了用户在数据库中的结构，包含以下字段：

-   `id`: 字符串类型，主键，使用 UUID 生成唯一标识符。
-   `username`: 字符串类型，最大长度 50，唯一，不可为空。用于用户登录。
-   `password`: 字符串类型，最大长度 100，不可为空。存储密码的哈希值。
-   `email`: 字符串类型，最大长度 100，可选。
-   `phone`: 字符串类型，最大长度 20，可选。
-   `created_at`: 日期时间类型，默认为当前时间。记录用户创建时间。
-   `real_name`: 字符串类型，最大长度 50，可选。用户真实姓名。
-   `id_card`: 字符串类型，最大长度 18，可选。身份证号。
-   `qq`: 字符串类型，最大长度 20，可选。QQ 号码。
-   `wechat`: 字符串类型，最大长度 50，可选。微信号码。
-   `wechat_openid`: 字符串类型，最大长度 100，可选。微信第三方登录 OpenID。
-   `qq_openid`: 字符串类型，最大长度 100，可选。QQ 第三方登录 OpenID。

## 3. 用户注册 (Registration)

注册功能通过 [`/register`](mysite/mainapp.py:50) 路由实现，支持 GET 和 POST 请求。

-   **GET 请求**: 渲染注册页面 [`register.html`](mysite/templates/register.html)。
-   **POST 请求**:
    -   获取表单提交的用户名、密码、确认密码、邮箱和手机号。
    -   检查用户名是否已存在。如果存在，通过 [`flash`](mysite/mainapp.py:61) 提示用户并重定向回注册页。
    -   验证密码和确认密码是否一致。如果不一致，通过 [`flash`](mysite/mainapp.py:66) 提示用户并重定向回注册页。
    -   使用 [`generate_password_hash`](mysite/mainapp.py:73) 对密码进行哈希处理。
    -   创建新的 [`User`](mysite/mainapp.py:70) 对象，使用 [`uuid.uuid4()`](mysite/mainapp.py:71) 生成唯一 ID。
    -   将新用户添加到数据库会话并提交。
    -   通过 [`flash`](mysite/mainapp.py:81) 提示用户注册成功，并重定向到登录页 [`/login`](mysite/mainapp.py:82)。
-   **前端特效**:
    -   注册数据项提示
    -   密码确认实时的一致检测和提示
    -   注册帐号实时的重名检测和提示
    -   注册按钮不满足条件禁用防误触

## 4. 用户登录 (Login)

登录功能通过 [`/login`](mysite/mainapp.py:87) 路由实现，支持 GET 和 POST 请求。

-   **GET 请求**: 渲染登录页面 [`login.html`](mysite/templates/login.html)。
-   **POST 请求**:
    -   获取表单提交的用户名和密码。
    -   根据用户名查询用户。
    -   如果用户存在，使用 [`check_password_hash`](mysite/mainapp.py:95) 验证提交的密码与数据库中存储的哈希密码是否匹配。
    -   如果验证成功，将用户 ID 和用户名存储在 [`session`](mysite/mainapp.py:96) 中，并重定向到首页 [`/`](mysite/mainapp.py:98)。
    -   如果验证失败（用户不存在或密码错误），通过 [`flash`](mysite/mainapp.py:100) 提示用户“用户名或密码错误”。

## 5. 用户注销 (Logout)

注销功能通过 [`/logout`](mysite/mainapp.py:105) 路由实现，支持 GET 请求。

-   从 [`session`](mysite/mainapp.py:107) 中移除用户 ID 和用户名。
-   重定向到首页 [`/`](mysite/mainapp.py:109)。

## 6. 个人信息管理 (Profile Management)

个人信息管理功能通过 [`/profile`](mysite/mainapp.py:112) 路由实现，支持 GET 和 POST 请求。

-   **访问控制**: 检查用户是否已登录（[`session.get('user_id')`](mysite/mainapp.py:114)）。如果未登录，通过 [`flash`](mysite/mainapp.py:115) 提示并重定向到登录页。
-   **GET 请求**:
    -   根据会话中的用户 ID 查询用户。
    -   渲染个人信息页面 [`profile.html`](mysite/templates/profile.html)，并将用户信息传递给模板。
-   **POST 请求**:
    -   根据会话中的用户 ID 查询用户。
    -   获取表单提交的各项个人信息字段（用户名、真实姓名、身份证号、手机号、QQ、微信、邮箱）。
    -   更新用户对象的相应字段。
    -   提交数据库会话。
    -   通过 [`flash`](mysite/mainapp.py:132) 提示用户个人信息已更新，并重定向回个人信息页。

## 7. 密码修改 (Change Password)

密码修改功能通过 [`/change_password`](mysite/mainapp.py:138) 路由实现，支持 GET 和 POST 请求。

-   **访问控制**: 检查用户是否已登录（[`session.get('user_id')`](mysite/mainapp.py:140)）。如果未登录，通过 [`flash`](mysite/mainapp.py:141) 提示并重定向到登录页。
-   **GET 请求**: 渲染密码修改页面 [`change_password.html`](mysite/templates/change_password.html)。
-   **POST 请求**:
    -   获取表单提交的旧密码、新密码和确认密码。
    -   根据会话中的用户 ID 查询用户。
    -   使用 [`check_password_hash`](mysite/mainapp.py:152) 验证提交的旧密码与数据库中存储的哈希密码是否匹配。如果验证失败，通过 [`flash`](mysite/mainapp.py:153) 提示并重定向回密码修改页。
    -   验证新密码和确认密码是否一致。如果不一致，通过 [`flash`](mysite/mainapp.py:158) 提示并重定向回密码修改页。
    -   使用 [`generate_password_hash`](mysite/mainapp.py:162) 对新密码进行哈希处理。
    -   更新用户对象的密码字段。
    -   提交数据库会话。
    -   通过 [`flash`](mysite/mainapp.py:165) 提示用户密码已成功更新，并重定向到个人信息页 [`/profile`](mysite/mainapp.py:166)。

## 8. 安全性

-   **密码存储**: 使用 [`werkzeug.security`](mysite/mainapp.py:5) 的 [`generate_password_hash`](mysite/mainapp.py:73) 对用户密码进行加盐哈希处理，而不是明文存储。
-   **密码验证**: 使用 [`check_password_hash`](mysite/mainapp.py:95) 安全地验证用户输入的密码与存储的哈希值。
-   **会话管理**: 使用 Flask 内置的 [`session`](mysite/mainapp.py:96) 来管理用户登录状态，会话数据默认存储在客户端的 Cookie 中，并经过签名以防止篡改。需要配置 `SECRET_KEY` 来确保会话安全。