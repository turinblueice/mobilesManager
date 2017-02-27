# -*- coding:utf8-*-

"""
doc:　登录.注册表单
Author:
date:
"""


from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):

    email = StringField(u'邮箱', validators=[DataRequired(u'请输入邮箱地址'), Email(u'邮箱地址错误')], render_kw={'placeholder': u'输入邮箱'})
    password = PasswordField(u'密码', validators=[DataRequired(u'请输入密码')])
    # next_auto_login = SelectField(u'下次自动登录',  option_widget=widgets.CheckboxInput(),
    #                               widget=widgets.ListWidget(prefix_label=False), choices=[(u'auto', u'下次自动登录')])
    next_auto_login = BooleanField(u'下次自动登录', render_kw={"checked":"checked"})
    submit = SubmitField(u'提交')


