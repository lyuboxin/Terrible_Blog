from utils.config import conf
import logging
from app import app
from flask_mail import Mail, Message

logger = logging.getLogger(__name__)

def send(to, title, content):
    logger.info('Send email {}:{}'.format(to, title))
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USERNAME'] = conf['emailname']
    app.config['MAIL_PASSWORD'] = conf['emailpassword'] 
    logger.info('Send email2 {}:{}'.format(to, title))
    mail = Mail(app)
    logger.info('Send email3 {}:{}'.format(to, title))
    msg = Message(title, sender=conf['emailname'], recipients=[to])
    msg.body = content
    logger.info('Send email4 {}:{}'.format(to, title))
    with app.app_context():
        mail.send(msg)

