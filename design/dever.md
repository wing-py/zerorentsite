# dever 开发者
website design docs for developer thing
该文档描述开发者相关页面的网站设计


# data_structure
## user
is_devlop # 是否是开发身份
is_custom # 是否是客户身份

github

dev_skills:[
    language: [
        python,
        c,
        java,
        c++,
        rust,
        nodejs,
        html/css/js,
    ],
    subject: [
        ai_rag,
        ai_model,
        router,
        website,
        wxuniapp,
        gamemod,
        game,
        broswer_extension,
        vscode_extension,
        microchip,
        ...
    ],
    tools: [
        kicad,
        keil,
        git,
        ...
    ],
    class: [
        pcb_design,
        3d_design,
        program,
        game_design,
        music_effect,
        figure_design,
    ],
]
description
note

preferences
category_preference  开发类目偏好: program,pcb-design,3d-model
language_preference  开发语言偏好: python,c,c++,js,html,css,rust
framework_preference 开发框架偏好: flutter
tool_preference      开发工具偏好: vscode,kicad,keil
applicant_preference 开发功能偏好: website,aiapi,ocr,llm
platform_preference  开发平台偏好: android,web,wxapp,windows,macos,isos,linux


skill-category:

### program:
language:python,c,c++,js,html,css,rust
tool:vscode,keil
framework:flutter
applicant:website,aiapi,ocr,llm
platform:android,web,wxapp,windows,macos,isos,linux


## project
id     # 数据项id
who    # 参与人id
job    # 参与工作
url    # 项目链接
name   # 项目名称
text   # 项目介绍,一个文本在/mysite/static/project/<project-id>.md

# user_operation
## 用户设置身份标记
在身份栏有设置用户是否是开发或客户的标记按钮，
1. “开发”标记按钮
点击“开发”按钮，会高亮该按钮，同时按钮右侧出现“编辑开发简历”的按钮
再次点击“开发”按钮，会熄灭该按钮，同时“编辑开发简历”的按钮消失
2. “客户”标记按钮
点击“客户”按钮，会高亮该按钮，同时按钮右侧出现“编辑客户简历”的按钮
再次点击“客户”按钮，会熄灭该按钮，同时“编辑客户简历”的按钮消失
## 浏览开发者名单
list_worker
显示注册用户数量，
显示所有注册用户，
传递数据表到前端，
按注册时间依次打印用户名和注册年月日。
## 注册项目
1. 编辑项目
1.1 添加项目
在开发简历编辑界面，
点击“注册项目”按钮弹出项目注册页面，
entry:
    项目名称
    参与方式
    项目链接
    项目介绍
填写好内容，点击“添加项目”会存储对应数据
1.2 删除项目
在开发简历编辑界面，
每个项目卡有“删除项目”红色按钮
1.3 修改项目
可以修改项目描述

profile.html的项目信息界面：
1.用户已经注册的项目信息区：
每个项目有一个卡片展示，
展示基本信息，
并有修改按钮和删除按钮
2.注册新项目的区域
点击注册项目按钮，弹出一个编辑界面
再次点击会隐藏
在编辑界面可以编辑信息，之后可以保存项目

# user_interface

## register_page

## profile_page