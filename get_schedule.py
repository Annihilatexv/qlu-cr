import datetime
import time
import pytz

# <<<<<!!!定义开学那周的周一!!!>>>>>
new_semester=[2023,2,20]
# <<<<<!!!考研时间!!!>>>>>
exam_day=[2023,12,23]


#获取当前教学周和星期数
def school_schedule():
    now_date,week_i=get_now_date()

    d1 = datetime.datetime(now_date[0],now_date[1],now_date[2])
    d2 = datetime.datetime(new_semester[0],new_semester[1],new_semester[2])
    # +1补足时间，+6向上取整
    weeks_now=((d1- d2).days+1+6)//7
    #print(weeks_now)

    # 获取周几 1-7
    #week_i = datetime.datetime.now().isoweekday()

    #week根据差值计算，week_i是实际星期几
    return weeks_now,week_i



# 获取考研倒计时
def exam_remain_day():
    now_date,week_i=get_now_date()

    d1 = datetime.datetime(now_date[0],now_date[1],now_date[2])
    d2 = datetime.datetime(exam_day[0], exam_day[1], exam_day[2])

    remain_days=d2-d1


    return [exam_day[0]+1,remain_days.days-1]

# 获取东八区日期
def get_now_date():
    tz = pytz.timezone("Asia/Shanghai")  # 东八区
    time_now = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone("Asia/Shanghai"))
    time_now=time_now+datetime.timedelta()
    dt=time_now.strftime("%Y,%m,%d")
    dt=[int (i) for i in dt.split(',')]

    return dt,time_now.isoweekday()


if __name__ == '__main__':
    print(school_schedule())
    print("%d届考研还有"%(exam_day+1),exam_remain_day(),"天")

