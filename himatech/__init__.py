from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app = Flask(__name__)
# make the SECRET_KEY an environment variable during production
app.config['SECRET_KEY'] = 'dr3t04ti03949i20r344nbijrnu4984e94023fmerv#$.rf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024  # 5Mb
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

login = LoginManager(app)
# login.login_view = 'login'
from himatech import routes,models
