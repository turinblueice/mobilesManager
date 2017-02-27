#　-*-coding:utf8-*-

"""
doc:  登录路由
author:
date
"""


import flask
from flask import Blueprint
from flask import render_template
from flask import session
from flask import request, flash, redirect, url_for
from flask import json
from app.forms import login_form

from app.models.model_users import Users


bp_login = Blueprint('login', __name__, template_folder='../templates')


@bp_login.route('/', methods=['get'])
def login_page():
    """
    访问登录页
    :return:
    """
    form = login_form.LoginForm()

    return render_template('login.html', title=u'登录', form=form)


@bp_login.route('/action/', methods=['post'])
def login_action():
    """
    登录操作
    :return:
    """

    form = login_form.LoginForm(request.form)

    if form.validate_on_submit():
        email = flask.escape(form.email.data)
        password = flask.escape(form.password.data)

        user = Users.query.filter_by(email=email).first()  #检索用户
        if user is not None:
            if password == user.password:  #用户名密码正确
                user_id = user.id
                session['user_id'] = str(user_id)  # 设置session和cookie
                session['nickname'] = user.nickname
                rsp = redirect('/index/'.format(user_id=user_id))

                if form.next_auto_login.data:  #  勾选下次自动登录则设置cookie
                    rsp.set_cookie('session_id', value=session['user_id'], max_age=3600*24)
                return rsp
            else:
                flash(u'密码错误', category='error')
        else:
            flash(u'用户名不存在', category='error')

    #  反馈提交登录资料的错误
    for errors in form.errors.values():
        for error in errors:
            flash(error, category='error')
    return redirect('/login/')


@bp_login.route('/out/action/', methods=['get'])
def logout_action():
    """
    登出
    :return:
    """
    session.pop('user_id', None)
    session.pop('nickname', None)
    rsp = redirect('/index/')
    rsp.delete_cookie('session_id')
    return rsp

