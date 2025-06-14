# zerorentsite
zero rent site for developer and order
domain_name:
[instance]
(https://zerorent.pythonanywhere.com/)

## copyleft
版权声明：采用GPL3.0版本扩散性开源协议
即可以免费商用，但使用该代码的软件需开源。

## 部署开发环境
### 1. python版本
生产环境为3.13.1

### 2. 安装package

以ubuntu上venv虚拟环境为例
`apt install python3 python3-pip python3-venv`
`python3 -m venv flask-venv`
`source flask-venv/bin/activate`

生产环境软件设施版本：
（如有需要，依次安装以下库：）
`pip install XX==version`
3.13.1_python:\
    Werkzeug==3.0.4
    Flask==3.0.3
    SQLAlchemy==2.0.36
    Flask-SQLAlchemy==3.1.1
    numpy==2.1.0
    pandas==2.2.2

## 相关资料
https://help.pythonanywhere.com/

## 对于vue分支代码，在zerorent-vue/下执行npm install安装相应工具，执行npm run build 编译代码到mysite/vue-build下
