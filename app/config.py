# -*- coding:utf8 -*-

"""
模块用法说明: 配置模块

Authors: Hong Quan(huojian@in66.com)
Date:
"""


import os


class Config(object):
    """
        app配置类
    """
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(BASE_DIR,  'app/static')
    STATIC_URL_PATH = '/app/static'


class DevelopmentConfig(Config):
    """
        开发环境配置
    """
    DEBUG = True  #app.debug
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'db/mobileManagerDB.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_WITH_PYCHARM = True  # use_reloader = False


class ProductionConfig(Config):
    """
        生产环境配置
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'db/mobileManagerDB.sqlite')


config = {

    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}