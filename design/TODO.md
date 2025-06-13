# TODO

# 添加称呼名
若未编辑称呼名(留空)
用户名默认为账号名，

账号名的作用是用于登录，
称呼名的作用是用于称呼。

账号名是唯一的，
但称呼名可以重复。

账号名 username
称呼名 callname

ALTER TABLE user ADD COLUMN callname VARCHAR(50) NULL;

# 开发者简历
## 添加接单声明
简要介绍自己对接单的偏好，
如怎样接单，接什么类型的单，
会走什么流程。

接单声明 order_claim

# 寻找开发者页面
## 添加<详情>按钮
每个用户条目有一个详情按钮，
点击详情按钮会跳转到用户介绍详情页。

view_user/<user_id>

# 发布订单
submit_order
## 类目
发布订单表单的<类目>input，
使用select，
options:
    网站搭建
    硬件研发
    移动应用
    软件开发
## 提示词
red message
请选择一个类目
green message
已选择订单类目"xxx"
## 联系方式
联系方式:
选择一种联系方式
    号码
    QQ
    微信
    邮箱
联系号码:


# 订单详情
提交、修改投标书
投标书公开可见
客户可以指定承包对象
提供合同模板


# 数据分离
main.index和main.progress的公告
信息存储到专门的数据文件，
而不是嵌入到html代码中。

