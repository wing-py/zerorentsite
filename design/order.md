# order 订单
website design docs for order thing
该文档描述订单相关处理的网站设计

# data_structure 数据结构
## user_submit_info 用户提交信息
class 类目
title 标题
description 描述
price 佣金
contact 联系
## auto_submit_info 自动提交信息
when(this order submit) 发布时间
who(submit this order) 发布用户
id 订单号
## talk_info 讨论信息
discuss_id 讨论号
comments: [ # 意见区
    who_comment  # 表达人
    what_comment # 意见陈述
]
## deal_info 交易信息
contract 合同
who_undertake: [] 承包方
## evaluate_info 双方评价信息
developer_evaluate_to_submiter 承包方对订单方的评价
submiter_evaluate_to_developer 订单方对承包方的评价


# user_operation 用户操作
1. add order 添加订单
2. list orders 罗列订单
3. del order 删除订单
4. edit order 修改订单
5. view order 查看订单详情
6. evaluate order 评价订单
   1. developer evaluate submiter
   2. submiter evaluate developer
7. comment 评论
8. discuss 讨论
9. contact submiter 联系订单方
10. filt orders 筛选订单


# user_interface 用户界面
## list_page 展览列表页面
add_order_button 添加订单按钮
order_list_info 所有订单展览列表
order_card_info 订单展示卡
    order_submit_info
    order_evaluate_info
    view_button 查看详情
    del_button 删除
    edit_button 修改
## form_page 提交表单页面
order_submit_form
    class
    title
    description
    price
    contact
## detail_page 订单详情页面
order_page_info
    order_submit_info
    order_comment_info
    order_comment_form
    evaluate_info
    evaluate_form

# todo
1. discuss
   添加即时讨论区
2. contract
   自动生成合同
3. filter
   根据条件筛选订单
4. recommend
   自动智能推荐