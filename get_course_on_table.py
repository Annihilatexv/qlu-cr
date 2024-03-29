import requests
from lxml import etree
import joblib
import json
import yaml
import pytz
import datetime
import time
import os

# 加载配置文件
def load_config():
    yaml_file = "config/config.yaml"
    with open(yaml_file, 'r',encoding='utf-8' ) as f:
        cfg = yaml.safe_load(f)
    return cfg

#定义获取当前时间的函数
def get_now_time():
    tz = pytz.timezone("Asia/Shanghai")  # 东八区
    time_now = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone("Asia/Shanghai"))
    
    year = time_now.year  # 年
    month = time_now.month  # 月
    day = time_now.day  # 日
    hour = time_now.hour  # 小时
    minute = time_now.minute  # 分钟
    
    return year, month, day, hour, minute


# 获取课表信息
def get_table(Cookie,table_url,district):

    # --------可能需要外部变量！
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4412.0 Safari/537.36 Edg/90.0.796.0',
        'Cookie': Cookie}
    #--------可能需要外部变量！
    data = {#'xnxqh': '2021-2022-2',
            'skyx': '',
            'xqid': district}

    course = requests.post(table_url, headers=headers, data=data)
    if "用户登录" in course.text:
        return []

    html = etree.HTML(course.text)
    result = html.xpath('//tr')
    # print(result)   #element对象的列表形式，

    table = []

    # 从第三行开始,前两行是星期和节数
    for tri in range(2, len(result)):
        td = result[tri].xpath('.//td/nobr')
        classroom_name = td[0].xpath('./text()')
        # print(classroom_name)

        tr_cell = [classroom_name]
        for tdi in range(1, len(td)):
            tr_cell.append(td[tdi].xpath('./div/text()'))

        # print(tr_cell)

        table.append(tr_cell)

    # print(table[0])
    return table

# 处理有课表，和教室表
def get_course_on_table(table):
    course_on_table = multidict()
    all_week = 7
    # --------可能需要外部变量！
    day_course = 6
    # 用于记录所有的教室名称，便于遍历
    all_classroom = []


    for tr in table:
        # 每行第一个cell是教室名
        classroom_name = tr[0][0]
        all_classroom.append(classroom_name)
        # print(classroom_name)

        # 剔除教室名，保留上课信息
        tr = tr[1:]

        # 每一行去除教室名，有42个cell=6*7
        # 先对星期几进行分组
        for week_i in range(all_week):  # (0-6)

            # 再对每天的第几节课进行分组，一天共有6节课
            for course_i in range(day_course):  # (0-5)
                # 根据上面的索引，计算出对应的cell
                cell = tr[week_i * day_course + course_i]  # 乘以6，因为每天只有6节课
                # 查询每个cell哪些周有课, 返回来的都是列表， week_on 是双层列表
                course_name_ls, tcher_name_ls, week_on, class_name_ls = cell_parse(cell)
                # print(classroom_name,week_on)

                # 按每个有课周写入对应的信息，最底层不为空即为有课， week_on 是双层列表
                for kind_i in range(len(week_on)):
                    for each_week in week_on[kind_i]:
                        # 先判断是否为空
                        # 为空新建
                        if not course_on_table[each_week][week_i + 1][course_i + 1][classroom_name]:
                            # 第几周，星期几，第几节课，教室名
                            course_on_table[each_week][week_i + 1][course_i + 1][classroom_name] = (
                            course_name_ls[kind_i], tcher_name_ls[kind_i], class_name_ls[kind_i])
                        # 不为空添加
                        else:
                            course_on_table[each_week][week_i + 1][course_i + 1][classroom_name] = tuple(
                                set([course_on_table[each_week][week_i + 1][course_i + 1][classroom_name],
                                     (course_name_ls[kind_i], tcher_name_ls[kind_i], class_name_ls[kind_i])]))

                # course_on_table[classroom_name][week_i+1][course_i+1]=(course_name,tcher_name,class_name)
                # print(set(week_on))
                # print(course_on_table[classroom_name][week_i+1][course_i+1])

    return course_on_table,all_classroom

def cell_parse(cell):
    # 保存每个cell中有课的周数
    week_on = []
    course_name_ls, tcher_name_ls, class_name_ls = [], [], []
    # 从每个单元3行3行判断
    for i in range(0, len(cell), 3):
        # i为每3行的头一行行数
        course_name = cell[i]
        tcher_name, week_name = cell[i + 1].split('\n')
        class_name = cell[i + 2]
        # print(week_name)
        week_on.append(week_name_parse(week_name, cell))
        course_name_ls.append(course_name)
        tcher_name_ls.append(tcher_name)
        class_name_ls.append(class_name)
    #         print(week_name)
    #         print(week_name_parse(week_name))
    #        print(week_on)
    return course_name_ls, tcher_name_ls, week_on, class_name_ls

# 进行周数的字符串解析
def week_name_parse(week_name, cell):
    # (1-16周), (5,12周),(1-8,10-17双周),(1-10单周),(2,4,6,8,10,14,16,18双周)

    week_on = []

    # 如果是单双周那么步长就会是2
    odd_even_step = 0
    if '单' in week_name:
        odd_even_step = 1
    elif '双' in week_name:
        odd_even_step = 2

    # 清除汉字，只保留数字进行识别
    week_name = week_name.replace('单', '').replace('双', '').replace('周', '').replace('(', '').replace(')', '')

    week_num = week_name.split(',')
    for each_num in week_num:
        # 连续周识别
        if '-' in each_num:
            start, end = each_num.split('-')
            # print(start,end)
            # 建立连续周数的列表，并进行单双周过滤
            num_list = [i for i in range(int(start), int(end) + 1)]

            if odd_even_step == 1:
                num_list = [i for i in num_list if i % 2]
            elif odd_even_step == 2:
                num_list = [i for i in num_list if not i % 2]

            week_on.extend(num_list)
        # 是孤立的周直接添加进来
        else:
            try:
                week_on.append(int(each_num))
            except:
                print('该单元可能有问题：', week_name, each_num, cell, sep='\n')
    return week_on

# 定义一个多层字典类
class multidict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


# 定义用于一个保存全校性课表的类
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.__str__()
        else:
            return super(MyEncoder, self).default(obj)

# 保存字典
def save_dict(dic,filename):
    with open(filename,'w',encoding='utf-8') as json_file:
        json.dump(dic, json_file, ensure_ascii=False, cls=JsonEncoder)

# 加载字典
def load_dict(filename):
    with open(filename,"r",encoding='utf-8') as json_file:
        dic = json.load(json_file)
    return dic

if __name__ == '__main__':
    #加载配置
    cfg = load_config()
    district_list={1:"changqing",3:"licheng",4:"heze"}

    # 添加对各容器的支持，检查环境变量是否存在
    if "table_url" in os.environ:
        table_url = os.environ["table_url"]
    else:
        table_url = cfg["string"]["table_url"]
    
    if "Cookie" in os.environ:
        Cookie = os.environ["Cookie"]
    else:
        Cookie = cfg["string"]["Cookie"]



    #遍历所有校区
    for district in district_list:
        print("<<<<<<<<%s校区>>>>>>>>>"%district_list[district])
        table=get_table(Cookie,table_url,district)
        if len(table):
            print("获取课表完成：", len(table))
        else:
            print("用户未登录，请检查 config/config.yaml 中Cookie！")
            exit()
        #print(table)

        course_on_table,all_classroom = get_course_on_table(table)
        print("处理教室与课表：",len(course_on_table), '\n所有教室：',all_classroom)

        # 保存课表字典
        print("正在保存到文件...")
        save_dict(course_on_table,"./static/data/course_on_table_%d.json"%district)
        # joblib.dump(course_on_table, './static/data/course_on_table.pkl',compress=3)
        joblib.dump(all_classroom, r'./static/data/all_classroom_%d.pkl'%district)
        print("保存成功！")



    # 保存时间戳
    print("正在保存时间戳到文件...")
    now_time = {"year": 0, "month": 0, "day": 0, "hour": 0, "minute": 0}
    now_time["year"], now_time["month"], now_time["day"], now_time["hour"], now_time["minute"] = get_now_time()
    with open("./static/data/modified_time.json" , "w") as f:
        json.dump(now_time, f)
    print("课表信息更新至",get_now_time())



    #print(course_on_table['1号公教楼JT102'][1][1])
    # print(course_on_table[3][1][1]['1号公教楼JT104'])
    #print(course_on_table.keys())


# unhashable type: 'list'
# 原因是列表是可变的type，而字典中的哈希类型必须是不可变得type，比如元组。