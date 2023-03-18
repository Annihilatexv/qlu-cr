from flask import (
    Flask,
    render_template,
    request
)
# from flask_bootstrap import Bootstrap5
import yaml

from qlu_lib import get_time, get_lib_seat
from query_classroom import query_room
from get_schedule import school_schedule, exam_remain_day



# 加载配置文件（无地安放2333）
def load_config():
    yaml_file = "config/config.yaml"
    with open(yaml_file, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    return cfg


cfg = load_config()
app = Flask(__name__)
# bootstrap = Bootstrap5(app)
# 2023考研倒计时
exam_time = exam_remain_day(cfg['list']['exam_day'])




@app.route("/")
def index():
    # 获取当前教学周和星期数，并进行html处理
    weeks, week_i = school_schedule(cfg['list']['new_semester'])

    weeks_list = {i: '' for i in range(1, 31)}
    weeks_list[weeks] = "selected"

    week_i_list = {i: '' for i in range(1, 8)}
    week_i_list[week_i] = "selected"

    # 获取时间和图书馆座位信息
    dt, hm, av_seat_list, un_seat_list= get_lib_seat()

    # render_template , 直接会在templates里边找xx.html文件
    return render_template("home.html", exam_time=exam_time, weeks=weeks_list, week_i=week_i_list, dt=dt, hm=hm,
                           av_seat_list=av_seat_list, un_seat_list=un_seat_list)




@app.route("/post", methods=["POST"])
def post():
    # 获取当前周数和星期
    weeks, week_i = school_schedule(cfg['list']['new_semester'])
    weeks, week_i = str(weeks), str(week_i)

    # 捕获收到的表单
    dic_form = request.form
    course_i = request.form.getlist('course_i[]')
    bro_agent = request.user_agent

    
    dt, hm = get_time()
    print('%s %s 从%s\n收到的表单为：\n' % (dt, hm, bro_agent), dic_form, course_i)



    # 日期处理：判断是否是否为本周/今天
    if weeks == dic_form['weeks'] :
        if week_i ==dic_form['week_i']:
            checked_date="今天 "   #今天 
        else:
            checked_date="本周 "+'星期' + dic_form['week_i'] 
    else:
            checked_date= '第' + dic_form['weeks']  + '周 '+'星期' + dic_form['week_i'] 
        


    # 课次处理
    co = "".join((lambda x: (x.sort(), x)[1])(course_i))
    course_info = ' 第'
    for i in co:
        course_info = course_info + str(int(i) * 2 - 1) + ('' if int(i) * 2 == 12 else str(int(i) * 2)) + ','
    course_info = course_info[:-1] + '节课'


    # 校区
    district = request.form['district']

    # 查询
    available_room = query_room( dic_form['weeks'], dic_form['week_i'] , course_i, cfg['list']['ban_list_{}'.format(district)], district)

    
    # 获取时间和图书馆座位信息
    dt, hm, av_seat_list, un_seat_list = get_lib_seat()

    return render_template("result.html",checked_date=checked_date, course_info=course_info,
                           available_room=available_room, av_seat_list=av_seat_list, un_seat_list=un_seat_list,
                           exam_time=exam_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=False)  # 修改代码会立即生效


