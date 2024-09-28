import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'auth_database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    if test_config is None: 
        # load the instance config, if it exists, when not testing  暂时没有config.py需求
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import auth
    app.register_blueprint(auth.bp)

    
    return app