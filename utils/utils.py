# -*-coding:utf8-*-

"""
公共模块
"""


def get_page_numbers(curr_page_number, per_page_items, page_count):
    """
    获取网页分页页码列表
    :param curr_page: 当前页号
    :param per_page_items:
    :param page_count:
    :return:
    """

    if page_count <= 0:  #总页码数为0，则说明无任何数据显示，展示页空白
        return [1]

    per_page_items = max(1, min(per_page_items, page_count))

    page_numbers_list = list()

    start_page = curr_page_number
    max_page_number = curr_page_number + per_page_items/2
    min_page_number = curr_page_number - per_page_items/2

    # 页码列表前后边界判定
    if page_count <= max_page_number:
        start_page = page_count - per_page_items + 1
    if 0 >= min_page_number:
        start_page = 1

    for index in xrange(per_page_items):
        page_numbers_list.append(index+start_page)

    return page_numbers_list

