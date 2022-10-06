import requests
import json

import time
import pytz
import datetime




import random
import os


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4706.0 Safari/537.36 Edg/98.0.1084.0",
    "Referer": "http://yuyue.lib.qlu.edu.cn"
}


def print_js(js):
    print(json.dumps(js, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))

def save_code(img_url,code_id,session=None):
    if session==None:
        img_response = requests.get(img_url, headers=headers)
    else:
        img_response = session.get(img_url, headers=headers)

    # img = Image.open(BytesIO(img_response.content))
    # img.show()
    with open('./static/code/code%d.png'%code_id,'wb') as f:
        f.write(img_response.content)




# 传入登录成功的session 返回验证码的路径
def get_code(session, headers): 

    headers["Referer"]="http://yuyue.lib.qlu.edu.cn"

    # 获取验证码
    check_url = "http://yuyue.lib.qlu.edu.cn/api.php/check"
    # 判断验证码图片是否存在
    code_id=0
    ## 如果要下面这一段，就注释这一行
    code_path ="./static/code/code%d.png"%code_id

    ## 避免验证码被覆盖，似乎用不到，如果需要，注释上面那行
    # while True:
    #     code_path ="./static/code/code%d.png"%code_id
    #     if os.path.exists(code_path):
    #         code_id=code_id+1
    #     else:
    #         break

    # 展示验证码图片
    save_code(check_url,code_id,session)

    return code_path




def login(session, headers, check_code):
    login_url = "http://yuyue.lib.qlu.edu.cn/api.php/login"
    data = {
        "username": "*******",
        "password": "*******",
        "verify": check_code,
    }

    login_info = session.post(login_url, headers=headers, data=data)
    # 返回登陆信息
    return login_info


# 获取东八区日期
def get_time(addday=0):
    tz = pytz.timezone("Asia/Shanghai")  # 东八区
    time_now = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone("Asia/Shanghai"))
    time_now=time_now+datetime.timedelta(days=addday)
    dt=time_now.strftime("%Y-%m-%d")
    hm=time_now.strftime("%H:%M")
    return [dt,hm]

#记得传列表
def is_available(count_list):
    for count in count_list:
        #print(count,type(count))
        if count==None or count==0:
            return False
    if count_list[0]==count_list[1]:
        return False
    return True


def query_seat(headers,area_id_list,time,print_info=False):
    #记录查询到的空座信息，装入字典列表 
    av_seat_dict=[]

    for area_id in area_id_list:
        #获得区域的segment
        segment=get_segment(headers,area_id,time[0])

        # 查询具体区域座位  area=7   day=2021-11-24   startTime=18:02    (endTime=21:30)
        seat_url='http://yuyue.lib.qlu.edu.cn/api.php/spaces_old?area={}&day={}&startTime={}&endTime=21:30'.format(area_id,time[0],time[1])
        seat_info=requests.get(seat_url,headers=headers)
        #print_js(seat_info.json())
        #座位列表
        seat_list=seat_info.json()['data']['list']
        
        
        # #座位布局图
        # pos_img='http://yuyue.lib.qlu.edu.cn/Public/home/images/web/area/%d/seat-free.jpg'%area_id
        # img_show(pos_img)

        #遍历找位 "临时离开":7   "空闲":1    "使用中":6   "已预约":2
        cnt=1
        for seat in seat_list:
            if seat['status_name']=="空闲":
                #添加空座信息
                av_seat_dict.append({
                    'id':seat['id'],
                    'no':seat['no'],
                    'name':seat['name'], #"4楼中走廊002",
                    'area':seat['area'],
                    'area_name': seat['area_name'], # "4楼中走廊"
                    'segment':segment
                })
                #打印操作
                if print_info:
                    print(seat['no'],end='\t')
                    #每10个换行
                    if cnt%10==0:
                        print()
                    cnt=cnt+1
                
    return av_seat_dict

def get_args(headers):
    ## 先登录吧，再查询，避免登录的时间内座位被抢
    # 创建session对象
    session = requests.Session()

    while True:
        code_url=get_code(session, headers)
        

        # 手动输入验证码，或许可以用神经网络？有空再说吧
        check_code = input()
        login_info = login(session, headers, check_code)

        print(login_info.json()['msg'])
        if login_info.json()['status']==1:
            break

    stu_info=login_info.json()['data']['list']
    print('{}的{}生\n{}，你好！'.format(stu_info['deptName'],stu_info['roleName'],stu_info['name']))





def query(time):
    url = "http://yuyue.lib.qlu.edu.cn/api.php/areas/1"

    response = requests.request("GET", url)
    a = response.cookies.items()
    b = ";".join('='.join(tup) for tup in a)

    # 楼层区域 信息
    total_url = "http://yuyue.lib.qlu.edu.cn/api.php/areas/0/date/%s" % time[0]
    
    # 或许在图书馆崩了的时候有所帮助
    try:
        # 需要session
        headers["Cookie"] = b
        total_info=requests.get(total_url,headers=headers,timeout=0.8)
    except:
        return [{'area_name': "当前响应过慢，不予访问，减少图书馆压力"}], [{'area_name': "当前响应过慢，不予访问，减少图书馆压力"}],''

    # 判断是否访问成功
    if total_info.status_code != 200:
        print(total_info.status_code, '图书馆已崩')
        return [{'area_name':"当前不可用。。"}], [{'area_name':"当前不可用。。"}]

    total_info=total_info.json()
    av_seat_list=[] #  记录每个区域空座信息，便于按楼层输出
    un_seat_list=[] #  记录每个区域非空座信息，便于按楼层输出
    for cd_area in total_info['data']['list']['childArea']:
        #cd_area['name'], ['TotalCount'], ['UnavailableSpace'], ['id'], ['parentId'] 
        # 排除大楼层（无用信息）
        if cd_area['parentId']>1: 
            # is_available其实可以不要了,因为已经排除 None 了 
            if is_available([cd_area['TotalCount'],cd_area['UnavailableSpace']]): #证明这里有座位
                available_num=int(cd_area['TotalCount'])-int(cd_area['UnavailableSpace'])
                av_seat_list.append({'area_id':"%02d"%cd_area['id'],'area_name':cd_area['name'].ljust(30),'available_num':available_num})
            else:
                un_seat_list.append({'area_id':"%02d"%cd_area['id'],'area_name':cd_area['name'],'available_num':0})

           

    # 按楼层排序
    name_sort=lambda x: x['area_name']
    av_seat_list.sort(key=name_sort)
    un_seat_list.sort(key=name_sort)


    # print('*'*30,'\n以下区域有座：\n','-'*30)
    floor_now=av_seat_list[0]['area_name'][0:1]


# 以下用于控制台打印座位信息
    # for f in av_seat_list:
    #     if floor_now!=f['area_name'][0:1]:
    #         print('-'*30)
    #         floor_now=f['area_name'][0:1]
        # print('{:>2d} : {} 剩余空座数:{}'.format(f['area_id'],f['area_name'],f['available_num']))
    

    # print('*'*30,'\n以下区域无座：\n','-'*30)
    # floor_now=un_seat_list[0]['area_name'][0:1]
    #
    # for f in un_seat_list:
    #     if floor_now!=f['area_name'][0:1]:
    #         print('-'*30)
    #         floor_now=f['area_name'][0:1]
    #     print('{:>2d} : {} '.format(f['area_id'],f['area_name']))
    
    return av_seat_list,un_seat_list,"剩余空座："



def get_segment(headers,area_id,dt):
    html=requests.get('http://yuyue.lib.qlu.edu.cn/api.php/areadays/%d'%area_id,headers=headers)
    area_date_list=html.json()['data']['list']
    for area_date in area_date_list:
        if area_date['day']==dt:
            return area_date['id']




def book_seat(session,headers,seat_id,userid,access_token,segment):
    book_url='http://yuyue.lib.qlu.edu.cn/api.php/spaces/%d/book'%seat_id
    data={
        'userid': userid,
        'access_token': access_token,
        'segment': segment,
        'type': '1'
    }
    #print('book_url',book_url)
    book_info=session.post(book_url,headers=headers,data=data)
    return book_info






def nowtime():
    # 报个时
    dt,hm=get_time()
    #print('当前日期:',dt,'\n当前时间:',hm)
    return dt,hm










def book_in(session,area_id_list,userid,access_token,headers,addday=0):

    #输入想去的区域id
    #area_id_list=input('输入你想要去的区域编号(多个输入用空格隔开)：')
    #area_id_list="8 9"

    area_id_list=list(int(i) for i in area_id_list.split(' '))

    

    #查询各个区域区域，得到可约座位字典列表
    av_seat_dict=query_seat(headers,area_id_list,get_time(addday))

    # 如果有位置
    if av_seat_dict:
        #随机选一个座位，看看是否需要其他方式，不过靠窗什么的写起来好麻烦，是来学习的，要求别那么多！
        tar_seat=random.choice(av_seat_dict)

        print(av_seat_dict)
        print('\n正在预约{} ...'.format(tar_seat['name']))

        # 抢座了 
        book_info=book_seat(session,headers,tar_seat['id'],userid,access_token,tar_seat['segment'])

        #打印预约结果
        print_js(book_info.json()['msg'])
        if book_info.json()['status']!=0:
            #座位布局图
            pos_img_url='http://yuyue.lib.qlu.edu.cn/Public/home/images/web/area/%d/seat-free.jpg'%tar_seat['area']
            return tar_seat['area_name']+tar_seat['no']+"预约成功！",book_info.json()['msg'].replace('<br/>','\t'),pos_img_url

        else:
             return "预约失败",book_info.json()['msg'],"https://img1.baidu.com/it/u=3192771932,2132972328&fm=224&fmt=auto&gp=0.jpg"
    # 所选区域没有位置 
    else:
        return "当前没有余座，继续检测"

    
