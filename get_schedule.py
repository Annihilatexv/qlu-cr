import datetime
import time
import pytz


def school_schedule():
    # 开学时间
    year,month,day=2022,2,28

    now_date,week_i=get_now_date()

    d1 = datetime.datetime(now_date[0],now_date[1],now_date[2])
    d2 = datetime.datetime(year, month, day)
    # +1补足时间，+6向上取整
    weeks_now=((d1- d2).days+1+6)//7
    #print(weeks_now)

    # 获取周几 1-7
    #week_i = datetime.datetime.now().isoweekday()
    return weeks_now,week_i



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

