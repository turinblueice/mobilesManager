# -*-coding:utf8 -*-

"""
主页模块
"""

import flask
from flask import Blueprint
from flask import render_template
from flask import make_response
from flask import request, flash, redirect, url_for
from flask import session
from app.forms import login_form
import hashlib
import re
import math

from utils import utils
from app.models.model_mobiles import Mobiles

bp_index = Blueprint('index', __name__, template_folder='../templates', static_folder='../static',
                     static_url_path='/index/static')


@bp_index.route("/", methods=['get'])
@bp_index.route("/index/", methods=['get'])
#@bp_index.route("/index/<int:mobile_page_num>/", methods=['post', 'get'])
def index_page():

    cookies = request.cookies
    session_id = cookies.get('session_id')   # 从用户cookie中获取session_id, cookie中字符已经过html encode
    session_id = session_id or ''

    user = None
    if 'user_id' in session and session_id == flask.escape(session['user_id']):
        user = session['nickname']

    # mobiles = Mobiles.query.all()
    # mobiles_infos = map(lambda mobile:{'mobile': mobile, 'image_path':'image/mobiles/'+mobile.thumbnail}, mobiles)
    # curr_page_num = request.args.get('page', '1')
    # curr_page_num = int(curr_page_num) if re.match("^\d+$", curr_page_num) else 1

    page = None
    try:
        page = int(request.args.get('page', 1))
    except (TypeError, ValueError):
        flask.abort(404)    # 分页参数错误则跳转404

    curr_page = page or 1

    query_str = request.args.get('query', None)
    if query_str is None:
        query_str = ''

    query_str = flask.escape(query_str).strip()
    if query_str:  # 加入搜索条件

        if query_str == 'available':  # 搜索语句等于available, 则为精确搜索库中的手机
            query_set = Mobiles.query.filter(Mobiles.borrower_id != None)
        else:
            comp = re.compile('.*(android|ios).*')
            result = comp.match(query_str)
            #  搜索条件有ios/android等词汇，则根据系统搜索
            if result:
                os_query = result.group(1)
                query_set = Mobiles.query.filter_by(os=os_query)
            else:  # 根据品牌搜索
                query_set = Mobiles.query.filter(Mobiles.brand.like("%"+query_str+"%"))
    else:
        query_set = Mobiles.query

    pagination = query_set.paginate(curr_page, 16, True)  # paginate已默认请求参数为page

    row_count = 3
    rows = [pagination.items[start:start+row_count] for start in xrange(0, len(pagination.items), row_count)]

    page_numbers = utils.get_page_numbers(pagination.page, 5, pagination.pages)

    rsp = make_response(render_template('index.html',
                                        user=user,  rows=rows, pagination=pagination,
                                        page_numbers=page_numbers))

    return rsp

