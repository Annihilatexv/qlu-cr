
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)

from qlu_lib import nowtime,get_time,query
from qury_classroom import  qury_room
from get_course_on_table import multidict,load_dict
from get_schedule import school_schedule
import sys,os
import requests

# render_template , 直接会在templates里边找xx.html文件




app = Flask(__name__)

@app.route("/")
def index():
    dt,hm=get_time()
    weeks,week_i=school_schedule()


    #查询总的空座信息
    try:
        av_seat_list,un_seat_list=query(get_time())
    except:
        av_seat_list, un_seat_list = ["似乎挂掉了。。。"], ["似乎挂掉了。。。"]

    return render_template("index.html",weeks=weeks,week_i=week_i,dt=dt,hm=hm ,av_seat_list=av_seat_list,un_seat_list=un_seat_list)




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

    weeks,week_i=school_schedule()
    weeks,week_i=str(weeks),str(week_i)
    available_room=[]

    # 捕获收到的表单
    dic_form= request.form

    if dic_form['weeks']:
        weeks=dic_form['weeks']
    if dic_form['week_i']:
        week_i=dic_form['week_i']

    #print("--%%%%%%%%---------------------\n", os.getcwd())
    # for root, dirs, files in os.walk(os.getcwd()):
    #     print('当前目录路径',root)  # 当前目录路径
    #     print('当前路径下所有子目录',dirs)  # 当前路径下所有子目录


    #course_on_table = load_dict(r"./static/data/course_on_table.json")

    available_room=qury_room(weeks,week_i,dic_form['course_i'])

    return render_template("result.html",dt=dt, hm=hm, available_room=available_room)





    
if __name__ == '__main__':
    app.run(debug=True) # 修改代码会立即生效
