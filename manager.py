#   -*- coding:utf8  -*-

import app

import flask_script
from flask_script import Manager
from flask_script import Server
from flask_script import Shell
from app.extensions import db

from utils import log


DEFAULT_APP_NAME = 'mobilesManagerSite'
curr_app = app.create_app(DEFAULT_APP_NAME,  'development')
manager = Manager(curr_app)

use_reloader = not(curr_app.config.get('DEBUG_WITH_PYCHARM'))
manager.add_command("runserver", Server(host='0.0.0.0', port=8000, use_reloader=use_reloader))

# def _mk_context():
#     return dict(db=db)
#
# manager.add_command('shell', Shell(make_context=_mk_context))


@manager.command
def createall():
    """
    创建数据库表
    :return:
    """
    from app.models.model_mobiles import Mobiles
    from app.models.model_users import Users

    db.create_all()
    print u'数据库创建完毕'


@manager.command
def dropall():
    """
    删除所有数据库表
    :return:
    """
    if flask_script.prompt_bool('are you sure?'):
        db.drop_all()


if __name__ == "__main__":

    manager.run()

