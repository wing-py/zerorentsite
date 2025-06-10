from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import os

forum_bp = Blueprint('forum', __name__)

here = os.path.dirname(os.path.abspath(__file__))
forum_static_path = os.path.join(os.path.dirname(here), 'static', 'forum')

# 论坛
## 论坛主页
@forum_bp.route('/forum')
def forum():
    topics = os.listdir(forum_static_path)
    return render_template('forum.html', topics=topics)

## 论坛话题
@forum_bp.route('/forum/topic/<topic_name>', methods=['GET', 'POST'])
def forum_topic(topic_name):
    # 获取话题的所有文件
    topic_path = os.path.join(forum_static_path, topic_name)
    if not os.path.exists(topic_path):
        flash('话题不存在')
        return redirect(url_for('forum.forum'))
    if request.method == 'POST':
            # 处理用户提交的内容
            #username = request.form.get('username') # 从表单获取用户名
            if not session.get('user_id'):
                flash('请先登录')
                return redirect(url_for('auth.login'))
            username = session.get('username')  # 从会话获取用户名
            content = request.form.get('content')

            if username and content:
                file_path = os.path.join(topic_path, username + '.txt')
                with open(file_path, 'w') as f:
                    f.write(content)
                return redirect(url_for('forum.forum_topic', topic_name=topic_name))
    # 获取该话题下的所有用户评论
    comments = []
    if os.path.exists(topic_path):
        for filename in os.listdir(topic_path):
            if filename.endswith('.txt'):
                username = filename[:-4]  # 去掉 .txt 扩展名
                with open(os.path.join(topic_path, filename), 'r') as f:
                    content = f.read()
                comments.append({'username': username, 'content': content})

    return render_template('topic.html', topic_name=topic_name, comments=comments)

