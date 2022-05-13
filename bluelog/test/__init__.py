import logging
import os

from logging.handlers import SMTPHandler,RotatingFileHandler

import click

from flask import Flask,render_template,request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import import blog_bp
from bluelog.extensions import bootstrap,db,login_manager,csrf,ckeditor,mail,moment,toolbar,migrate
from bluelog.models import Admin,Post,Category,Comment,Link
from bluelog.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')
    app =Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app）
    retister_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context()
    register_template_context(app)
    register_request_handlers(app)
    return app

def register_logging(app):
    class RequestFormatter(logging.Formatter):
        def format(self,record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter,self).format(record)
    request_formatter = RequestFormatter(
        '[%(asctime)s]%(remote_ddr)s requested %(url)s\n'
        '%(levelname)s in %(module)s:%(message)s'
        )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')

    file_handler = RotaingFileHandler(os.path.join(basedir,rmat'logs/bluelog.log'),
                    maxBytes = 10*10224*1024,backupcCount = 10)
    file_handler.setFormatter(formatter)
    file_hanlder.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost = app.config['MAIL_SERVER'],
        fromaddr = app.config['MAIL_USERNAME'],
        toaddrs = ['ADMIN_EMAIL'],
        subject = 'Bluelog Application Error',
        credentials = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD']))
        mail_handler.setLEvel(logging.ERROR)
        mail_hanlder.setFOrmatter(request_formatter)


        if not app.debug:
            app.logger.addHandler(mail_handler)
            app.logger.addHandler(file_handler)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.inti_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app,db)

def register_blueprint(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix = '/auth')



