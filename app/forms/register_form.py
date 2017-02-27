# -*- coding:utf8-*-

"""
doc:　登录.注册表单
Author:
date:
"""


from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms import widgets
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(Form):

    email = StringField(u'邮箱', validators=[DataRequired(u'请输入邮箱地址'), Email(u'邮箱地址错误')], render_kw={'placeholder': u'输入邮箱'})
    password = PasswordField(u'密码', validators=[DataRequired(u'请输入密码'), Length(min=5, max=10, message=u'密码长度5到10个字符')])
    password_confirm = PasswordField(u'确认密码', validators=[DataRequired(u'请再次确认输入密码')])
    nick_name = StringField(u'花名', validators=[DataRequired(u'输入你的花名')], render_kw={'placeholder': u'花名'})
    submit = SubmitField(u'提交')


