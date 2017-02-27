# -*- coding:utf8 -*-


from app import config
from flask import Flask
from app import extensions
from app import views
from app import globals as gl


DEFAULT_MODULE = (
    (views.bp_index, ''),
    (views.bp_login, '/login'),
    (views.bp_register, '/register'),
    (views.bp_mobile, '/mobile')
)


def create_app(app_name, config_name, modules=None):

    app = Flask(app_name)
    app.config.from_object(config.config[config_name])

    modules = modules or DEFAULT_MODULE
    configure_blueprint(app, modules)
    configure_extensions(app)
    configure_global_functions(app)

    return app


def configure_blueprint(app,  modules):

    if isinstance(app, Flask):
        for module,  url_prefix in modules:
            app.register_blueprint(module, url_prefix=url_prefix)


def configure_extensions(app):

    if isinstance(app, Flask):
        extensions.db.init_app(app)


def configure_global_functions(app):

    if isinstance(app, Flask):
        app.add_template_global(gl.get_borrower_name, 'get_borrower_name')