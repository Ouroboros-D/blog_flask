from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort
from .auth import roles_required
from .datebase import User,Post
from . import db

bp = Blueprint('blog', __name__)


#@roles_required('admin', 'user','guest') 登录检验

@bp.route('/')
def index():
    # 查询所有的帖子，并根据创建时间降序排列
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=['GET', 'POST'])
@roles_required('admin', 'user')  # 确保用户登录才能创建博客
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        # 检查标题和内容是否为空
        if not title or not body:
            flash('Title and Body are required!')
            return render_template('blog/create.html')

        # 创建一个新的Post实例并保存到数据库
        user_id = session['user_id']
        new_post = Post(title=title, body=body, author_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        flash('Blog post created successfully!')
        return redirect(url_for('blog.index'))  # 创建成功后重定向到博客列表页面

    return render_template('blog/create.html')