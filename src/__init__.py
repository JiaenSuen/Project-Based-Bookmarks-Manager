# src/__init__.py
from flask import Flask
from .config import DevelopmentConfig  
from .extensions import db


from .models.project import Project
from .models.bookmark import Bookmark

def create_app():
    app = Flask(__name__,
                instance_relative_config=True)

    app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    import os
    os.makedirs(app.instance_path, exist_ok=True)

    with app.app_context():
        try:
            db.create_all()
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
        except Exception as e:
            print("Error when building database : ", str(e))

    from .blueprints.web.routes import web_bp
    app.register_blueprint(web_bp)
    return app