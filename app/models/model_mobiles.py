# -*-coding:utf8-*-

from app.extensions import db
from app.models.model_users import Users


class Mobiles(db.Model):
    """
    手机信息
    """

    __tablename__ = 'mobiles'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement='auto')

    brand = db.Column('brand', db.String(10),  nullable=False)  # 手机品牌
    model = db.Column('model', db.String(20), nullable=False)  # 手机型号

    os = db.Column('os', db.String(10), nullable=False)  # 操作系统 ios/android
    version = db.Column('version', db.String(10), nullable=False)  # 系统版本

    cpu = db.Column('cpu', db.String(20)) # CPU品牌
    cpu_model = db.Column('cpu_model', db.String(20)) # CPU型号

    rom = db.Column('rom', db.Integer) # rom 存储空间大小
    ram = db.Column('ram', db.Integer) # ram 运存

    size = db.Column('size', db.Float) # 屏幕尺寸，单位英寸，如5.7
    resolution = db.Column('resolution', db.String(20)) # 分辨率

    thumbnail_path = db.Column('thumbnail', db.String(50)) # 缩略图路径

    borrower_id = db.Column('borrower_id', db.Integer, db.ForeignKey('users.id'))  # 外键
    borrower = db.relationship(Users, backref=db.backref('mobiles', lazy='dynamic')) # 外键关系

    def __init__(self, brand, model, os, version, cpu=None, cpu_model=None, rom=None,
                 ram=None, size=None, resolution=None, thumbnail_path=None, borrower_id=1):
        self.brand = brand
        self.model = model
        self.os = os
        self.version = version
        self.cpu = cpu or ''
        self.cpu_model = cpu_model or ''
        self.rom = rom or 0
        self.ram = ram or 0
        self.size = size or 0.0
        self.resolution = resolution or ''
        self.thumbnail_path = thumbnail_path or ''
        self.borrower_id = borrower_id

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

        infos = (self.os, self.brand, self.model, self.version)
        for index, attr in enumerate(infos):
            if isinstance(attr, unicode):
                infos[index] = attr.encode('utf8')

        return '系统:{};品牌{};型号{};版本{}'.format(*infos)