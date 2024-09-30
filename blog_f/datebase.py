from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # 用户角色

    # 增加一个与 Post 的关系。`backref` 让 Post 也能访问 User
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    # author_id 是外键，关联到 User 的 id
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
