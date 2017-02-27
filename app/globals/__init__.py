# -*-coding:utf8-*-
"""
自定义模板全局函数模块
"""


from app.models.model_users import Users


def get_borrower_name(borrower_id):
    """
    获取手机借用者姓名
    :return:
    """
    borrower_id = int(borrower_id)
    user = Users.query.filter_by(id=borrower_id).first()

    return '' if user is None else user.nickname
