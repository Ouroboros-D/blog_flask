from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
@bp.route('/dashboard')
def dashboard():
    user_role = session.get('role')
    if not user_role:
        return redirect(url_for('auth/login'))  # 如果没有登录，重定向到登录页面
    
    if user_role == 'admin':
        # 渲染管理员页面或内容
        return render_template('dashboard.html', role='admin')
    elif user_role == 'user':
        # 渲染普通用户页面或内容
        return render_template('dashboard.html', role='user')
    else:
        # 渲染访客页面或内容
        return render_template('dashboard.html', role='guest')