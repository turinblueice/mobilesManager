# -*-coding:utf8-*-

from app.extensions import db


class Users(db.Model):
    """
    用户信息
    """

    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement='auto')

    email = db.Column('email', db.Text,  nullable=False)  # 邮箱
    password = db.Column('password', db.String(11), nullable=False)  # 密码
    nickname = db.Column('nickname', db.String(20), nullable=False)  # 花名

    def __init__(self, email, password, nickname):
        self.email = email
        self.password = password
        self.nickname = nickname

    def save(self, lazy=False):
        """
        将该数据保存到数据库
        :param lazy: True:延迟提交到数据库；False: 立即提交到数据库
        :return:
        """
        db.session.add(self)
        if not lazy:
            db.session.commit()


    def discard(self, lazy=False):
        """
        将该数据删除
        :param lazy: True:延迟提交到数据库；False: 立即提交到数据库
        :return:
        """
        db.session.delete(self)
        if not lazy:
            db.session.commit()

    @staticmethod
    def update():
        """
        提交更改
        :return:
        """
        db.session.commit()

    def __str__(self):
        """
        打印出花名
        :return:
        """
        nickname = self.nickname
        if isinstance(nickname, unicode):
            nickname = nickname.encode('utf8')
        return nickname
