from blog_f import create_app, db  # 导入你的 Flask 应用和 db 对象

app = create_app()  # 使用应用工厂创建 Flask 应用实例

# 在应用上下文中执行 db.create_all()
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")