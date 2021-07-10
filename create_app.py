from flask import Flask


def create_miri():
    app = Flask(__name__)
    from app.db_operations.miri_db import miri_module
    app.register_blueprint(miri_module)
    return app