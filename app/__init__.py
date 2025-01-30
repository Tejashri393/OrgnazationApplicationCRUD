from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

db = SQLAlchemy()


# Load config from config.py
app.config.from_pyfile('config.py')
db.init_app(app)

from app.controller.org import org_bp
from app.controller.emp import employee_bp
from app.controller.roles import role_bp
app.register_blueprint(org_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(role_bp)

@app.route('/')
def index():
    return "Welcome to Organization Management API!"