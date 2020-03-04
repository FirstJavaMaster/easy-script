import requests
from bs4 import BeautifulSoup, Tag

# 自增长的id
last_id = 0


def run():
    resp = requests.get(r'https://www.kuaidaili.com/doc/dev/china_area_code/')
    soup = BeautifulSoup(resp.text, 'lxml')
    article_tag = soup.find(id='content').find('article')

    # 中国节点
    china = Area('中国', '000000')

    # 定义从0开始的游标
    index = 0
    # 定义一个暂存区
    province_tag = None

    for child_tag in article_tag.children:
        if not_tag(child_tag):
            continue

        index += 1
        if index <= 2:
            continue

        if index % 2 == 1:
            province_tag = child_tag
        else:
            deal_province(province_tag, child_tag, china)

    area_list = []
    to_list(area_list, china, None)
    to_csv(area_list)


def to_csv(area_list):
    content = 'id\tname\tcode\tparent_id\tdepth\tpath\n'
    for area in area_list:
        this_line = '%s\t%s\t%s\t%s\t%s\t%s\n' % (area.id, area.name, area.code, area.parent_id, area.depth, area.path)
        content = content + this_line

    with open('/tmp/area.csv', 'w', encoding='utf-8') as file:
        file.write(content)
        file.close()


def to_list(area_list, area, parent):
    global last_id
    last_id = last_id + 1

    area.id = last_id
    area.parent_id = 0 if parent is None else parent.id
    area.depth = 1 if parent is None else parent.depth + 1
    area.path = str(area.id) if parent is None else parent.path + '-' + str(area.id)
    area_list.append(area)

    if len(area.children) > 0:
        for child in area.children:
            to_list(area_list, child, area)


def deal_province(province_tag, province_child_tag, china):
    if province_tag is None or province_child_tag is None:
        raise Exception('省份数据解析异常')

    province = get_name_and_code(province_tag.string)
    china.children.append(province)

    for city_tag in province_child_tag.find('ul', recursive=False).children:
        if not_tag(city_tag):
            continue
        deal_city(city_tag, province)


def deal_city(city_tag, province):
    city = get_name_and_code(city_tag.find('h5').string)
    province.children.append(city)

    for town_tag in city_tag.find_all('li'):
        if not_tag(town_tag):
            continue
        deal_town(town_tag, city)


def deal_town(town_tag, city):
    town = get_name_and_code(town_tag.string)
    city.children.append(town)


def not_tag(obj):
    return not isinstance(obj, Tag)


def get_name_and_code(string):
    items = string.split()

    lack_of_number = 6 - len(items[1])
    code = items[1] + '0' * lack_of_number
    return Area(items[0], code)


class Area:
    id = None
    name = None
    code = None
    parent_id = None
    depth = None
    path = None
    children = None

    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.children = []


if __name__ == '__main__':
    run()
