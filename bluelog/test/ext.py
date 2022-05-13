from flask_bootstrap import Bootstrap4
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate

bootStrap = Bootstrap4()
db = SQLAlchemy()
login_manager = LoginManager()
crsf = CSRFProtect()
ckedirot = CKEditor()
mail = Mail()
moment = Moment()
toobar = DebugToolbarExtension()
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user

login_manager.login_view='auth.login'
login_manager.login_message_category = 'warning'
