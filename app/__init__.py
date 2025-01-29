from flask import Flask
from app.Model.org import db
from app.controller.org import org_bp
from app.Model.emp import db
from app.controller.emp import employee_bp


app = Flask(__name__)

# Load config from config.py
app.config.from_pyfile('config.py')
db.init_app(app)
app.register_blueprint(org_bp)
app.register_blueprint(employee_bp)

@app.route('/')
def index():
    return "Welcome to Organization Management API!"