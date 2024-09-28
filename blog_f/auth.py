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
        role = request.form.get('role', 'user')  # 从表单获取角色，默认是user
        new_user = User(username=username, password=password, role=role)
    try:
        new_user = User(username='bossxu', password='your_hashed_password', role='admin')
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("用户名已存在，插入操作已忽略")

        return redirect(url_for('auth.login'))
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
            
            # 根据角色跳转到不同的页面
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'user':
                return redirect(url_for('user_dashboard'))
            else:
                return redirect(url_for('guest_dashboard'))
        else:
            # 如果验证失败，闪现错误消息
            flash('Login failed. Check your username and password.', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('You need to be logged in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('role') != role:
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
