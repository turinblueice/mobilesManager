#　-*-coding:utf8-*-

"""
doc:  注册路由
author:
date
"""
import flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request, flash, redirect, url_for
from flask import json
from app.forms import register_form

from utils import log
from app.models.model_users import Users


bp_register = Blueprint('register', __name__, template_folder='../templates')


@bp_register.route('/', methods=['get'])
def register_page():
    """
    访问登录页
    :return:
    """
    form = register_form.RegisterForm()

    return render_template('register.html', title=u'注册', form=form)


@bp_register.route('/action/', methods=['post'])
def register_action():
    """
    注册操作
    :return:
    """

    form = register_form.RegisterForm(request.form)

    if form.validate_on_submit():
        email = flask.escape(form.email.data)
        password = form.password.data
        password_confirm = form.password_confirm.data
        nick_name = form.nick_name.data

        user = Users.query.filter_by(email=email).first()
        if user is None:
            user = Users.query.filter_by(nickname=nick_name).first()
            if user is None:  # 花名未注册
                if password == password_confirm:
                    log.logger.info("开始添加新注册的用户")
                    user = Users(email, password, nick_name)
                    user.save()
                    log.logger.info("用户\"{}\"注册成功".format(email.encode('utf8')))
                    user_id = user.id
                    session['user_id'] = str(user_id)  # 设置session和cookie
                    session['nickname'] = nick_name
                    rsp = redirect('/index/')
                    rsp.set_cookie('session_id', value=session['user_id'], max_age=3600*24)
                    return rsp
                else:
                    log.logger.error("两次输入的密码不同")
                    flash(u'两次输入的密码不同',  category='error')
            else:
                log.logger.error("\"{}\"花名已经注册".format(nick_name.encode('utf8')))
                flash(u'花名已注册',  category='error')
        else:
            log.logger.error("\"{}\"用户已注册".format(email.encode('utf8')))
            flash(u'用户名已注册',  category='error')


    # 反馈提交登录资料的错误
    for errors in form.errors.values():
        for error in errors:
            flash(error, category='error')
    return redirect('/register/')

