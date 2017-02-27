# -*-coding:utf8 -*-

"""
手机详情模块
"""

import flask
from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import Response
from flask import request, flash, redirect, url_for
from flask import session
from flask import json
from app.forms import login_form
import hashlib

from app.models.model_users import  Users
from app.models.model_mobiles import Mobiles


bp_mobile = Blueprint('mobile', __name__, template_folder='../templates')


@bp_mobile.route("/<int:mobile_id>/", methods=['get'])
def mobile_info_page(mobile_id=None):
    """
    访问手机详细信息页
    :param mobile_id: 手机数据库编号
    :return:
    """
    cookies = request.cookies
    session_id = cookies.get('session_id')   # 从用户cookie中获取session_id, cookie中字符已经过html encode
    session_id = session_id or ''

    # 根据传入的mobile_id获取mobile信息
    mobile = Mobiles.query.filter_by(id=mobile_id).first()
    owner_nickname = None
    is_borrower = False
    if mobile.borrower_id:
        owner = Users.query.filter_by(id=mobile.borrower_id).first()
        owner_nickname = owner.nickname
        if session.get('user_id'):
            is_borrower = True if session['user_id'] == str(owner.id) else False

    user = None
    if 'user_id' in session and session_id == flask.escape(session['user_id']):  # 获取当前登录的用户信息
        user = session['nickname']

    rsp = make_response(render_template('mobile-info.html',
                                        user=user, is_borrower=is_borrower, mobile=mobile, owner=owner_nickname))

    return rsp


@bp_mobile.route("/borrow/", methods=['post'])
def borrow_mobile_action():
    """
    借手机操作
    :return:
    """
    _rsp = dict(succ=0)
    mobile_id = request.form.get('mobile_id', None)
    curr_id = session.get('user_id', None)  # 从session中获取用户信息
    if curr_id:  # 当前为登录状态，当前session中有user_id的用户信息

        # 校验mobile_id
        try:
            mobile_id = int(mobile_id)
        except (ValueError, TypeError):
            flask.abort(404)

        mobile = Mobiles.query.filter_by(id=mobile_id).first()
        mobile.borrower_id = curr_id
        mobile.update()
        _rsp['message'] = u'已完成借用登记'
        _rsp['curr_borrower_id'] = curr_id
    else:
        _rsp['succ'] = 1
        _rsp['message'] = u'请先登录'

    return Response(json.dumps(_rsp), content_type='application/json')


@bp_mobile.route('/give-back/', methods=['post'])
def give_back_mobile_action():
    """
    归还手机
    :return:
    """
    _rsp = dict(succ=0)
    mobile_id = request.form.get('mobile_id', None)
    curr_id = session.get('user_id', None)  # 从session中获取当前用户信息
    if curr_id:
        # 当前为登录状态，当前session中有user_id的用户信息

        # 校验mobile_id
        try:
            mobile_id = int(mobile_id)
        except (ValueError, TypeError):
            flask.abort(404)

        mobile = Mobiles.query.filter_by(id=mobile_id).first()
        if mobile.borrower_id == int(curr_id):
            mobile.borrower_id = None  # 归还手机
            mobile.update()
            _rsp['message'] = u'已成功归还'
            _rsp['curr_borrower_id'] = 0
        else:
            _rsp['succ'] = 2
            _rsp['message'] = u'要归还的手机不在当前用户手上'
            _rsp['curr_borrower_id'] = mobile.borrower_id
    else:
        _rsp['succ'] = 1
        _rsp['message'] = u'请先登录'

    _rsp['curr_borrower_id'] = curr_id or 0
    return Response(json.dumps(_rsp), content_type='application/json')