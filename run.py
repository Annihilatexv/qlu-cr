from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)

from qlu_lib import get_time,get_lib_seat
from query_classroom import  query_room
from get_schedule import school_schedule,exam_remain_day
import yaml

# 加载配置文件（无地安放2333）
def load_config():
    yaml_file = "config/config.yaml"
    with open(yaml_file, 'r',encoding='utf-8' ) as f:
        cfg = yaml.safe_load(f)
    return cfg
cfg = load_config()


app = Flask(__name__)

@app.route("/")
def index():

    weeks,week_i=school_schedule(cfg['list']['new_semester'])

    # 获取时间和图书馆座位信息
    dt, hm, av_seat_list, un_seat_list,seat_sign=get_lib_seat()

    #2023考研倒计时
    exam_time = exam_remain_day(cfg['list']['exam_day'])

    # render_template , 直接会在templates里边找xx.html文件
    return render_template("index.html",exam_time=exam_time,weeks=weeks,week_i=week_i,dt=dt,hm=hm ,av_seat_list=av_seat_list,un_seat_list=un_seat_list,seat_sign=seat_sign)

@app.route("/get")
def get():
    #data["url"] = request.url
    # get方法获取到的参数
    #name = request.args.get('name','zhangsan')

    #request.args
    #data["remote_addr"] = request.remote_addr

    return render_template("index.html")


@app.route("/post", methods=["POST"])
def post():
    dt, hm = get_time()
    is_today =1

    # 获取当前周数和星期
    weeks,week_i=school_schedule(cfg['list']['new_semester'])
    weeks,week_i=str(weeks),str(week_i)


    # 捕获收到的表单
    dic_form= request.form
    course_i = request.form.getlist('test[]')
    bro_agent=request.user_agent
    print('%s %s\n从%s\n收到的表单为：\n'%(dt, hm,bro_agent),dic_form,course_i,'\n')


    # 判断是否为今天
    if dic_form['weeks']:
        weeks=dic_form['weeks']
        is_today = 0
    if dic_form['week_i']:
        week_i=dic_form['week_i']
        is_today = 0


    available_room=query_room(weeks,week_i,course_i,cfg['list']['ban_list'])
    # 查询完后时间信息进行处理显示
    if is_today:
         today= '今天'
         weeks,week_i='',''
    else:
        today=''
        weeks='第'+weeks+'周'
        week_i='星期'+week_i



    co = "".join((lambda x: (x.sort(), x)[1])(course_i))
    course_i='第'
    for i in co:
        course_i=course_i+str(int(i)*2-1)+('' if int(i)*2==12 else str(int(i)*2))+','
    course_i=course_i[:-1]+'节课'

    # 获取时间和图书馆座位信息
    dt, hm, av_seat_list, un_seat_list,seat_sign=get_lib_seat()


    return render_template("result.html",dt=dt, hm=hm,weeks=weeks,week_i=week_i,course_i=course_i,today=today, available_room=available_room ,av_seat_list=av_seat_list,un_seat_list=un_seat_list,seat_sign=seat_sign)


if __name__ == '__main__':

    app.run(debug=True) # 修改代码会立即生效
    

