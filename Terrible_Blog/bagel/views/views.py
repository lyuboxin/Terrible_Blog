from  .auth import auth_blueprint
from .user import user_blueprint
from .post import post_blueprint
from app import app

app.register_blueprint(blueprint=auth_blueprint, url_prefix='/auth')
app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
app.register_blueprint(blueprint=post_blueprint, url_prefix='/post')
