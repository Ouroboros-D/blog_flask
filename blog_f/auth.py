from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError

from .datebase import User
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form.get('role', 'user')  # 获取角色，默认是user

        # 使用表单数据创建用户实例
        new_user = User(username=username, password=password, role=role)

        try:
            db.session.add(new_user)  # 将新用户添加到会话
            db.session.commit()       # 提交会话，将数据写入数据库
        except IntegrityError:
            db.session.rollback()  # 如果用户名已存在，回滚事务
            print("用户名已存在，插入操作已忽略")
            flash('Username already exists.', 'error')  # 提示用户用户名已存在
            return render_template('auth/register.html')  # 返回注册页面以便用户重新输入

        # 注册成功后重定向到登录页面
        return redirect(url_for('auth.login'))

    # 如果是 GET 请求，渲染注册页面
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 从表单中获取用户名和密码
        username = request.form['username']
        password = request.form['password']
        
        # 查询数据库，查找对应用户名的用户
        user = User.query.filter_by(username=username).first()
        
        # 检查用户是否存在，以及密码是否正确
        if user and check_password_hash(user.password, password):
            # 验证成功后，存储用户信息到 session 中
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role  # 存储角色信息
            
            flash(f'Welcome, {user.username}!', 'success')
            
            return redirect(url_for('blog.create'))

            # 根据角色跳转到不同的页面
            if user.role == 'admin':
                return redirect(url_for('dashboard'),role='admin')
            elif user.role == 'user':
                return redirect(url_for('dashboard'),role='user')
            else:
                return redirect(url_for('dashboard'),role='guset')
        else:
            # 如果验证失败，闪现错误消息
            flash('Login failed. Check your username and password.', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

def roles_required(*roles):  # 接受多个角色
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('You need to be logged in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            user_role = session.get('role')
            if user_role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@bp.route('/logout')
def logout():
    
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
