import flask
import flask_bootstrap
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

App = flask.Flask(__name__)
App.secret_key = 'asjdkaq343asad'

# Bootstrap-Flask requires this line
bootstrap = flask_bootstrap.Bootstrap4(App)
# Flask-WTF requires this line
csrf = CSRFProtect(App)

db_name = 'sqllite.db'

App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

DB = SQLAlchemy(App)
