import joblib
from get_course_on_table import multidict,load_dict
import json
import sys,os
# 查找空教室


# for i in all_classroom:
#     print(i)





def query_room(week_now,week_i_now,course_i_now):
    all_week = 7
    day_course = 6
    available_room=[]


    # 加载已保存的课表
    #course_on_table = joblib.load(r"./static/data/course_on_table.json")

    all_classroom = joblib.load(r'./static/data/all_classroom.pkl')
    course_on_table = load_dict("./static/data/course_on_table.json")

    week_now = [i for i in week_now.split()]
    week_i_now = [i for i in week_i_now.split()]
    course_i_now = [i for i in course_i_now]


    # 查找所有教室中，对应时间无课的
    for classroom in all_classroom:
        is_available = 1
        for each_week in week_now:
            for each_week_i in week_i_now:
                for course_i in course_i_now:
                    try:
                        # 如果有课直接跳出
                        if course_on_table[each_week][each_week_i][course_i][classroom]:
                            is_available = 0
                            break
                    except:
                        pass
        # 所查询时间段都无课
        if is_available:
            #print(classroom)
            available_room.append(classroom)



    # 处理不能进的空教室
    ban_list = ['北楼', '语言', '办公', '3号', '同声', '机房', '同声传译', '实验北楼', '操场', '室','1号公教楼405','1号公教楼305','1号公教楼505','1号公教楼604','2号公教楼201','2号公教楼202','2号公教楼203']
    available_room_filtered = []

    for room in available_room:
        for ban in ban_list:
            if ban in room:
                break
        else:
            available_room_filtered.append(room)

    available_room_pretty=pretty(available_room_filtered)

    return available_room_pretty

def pretty(available_room_filtered):
    available_room_filtered = sorted(available_room_filtered, key=str.swapcase)
    # available_room = sorted(available_room,key= lambda i:i[0])

    available_room_pretty = ['————————————————', available_room_filtered[0]]

    # 美化一下
    for i in range(1, len(available_room_filtered)):
        if available_room_filtered[i][0] != available_room_filtered[i - 1][0]:
            available_room_pretty.append('————————————————')

        elif "JT" in available_room_filtered[i] and "JT" not in available_room_filtered[i - 1]:
            available_room_pretty.append('------------------------')
        available_room_pretty.append(available_room_filtered[i])
    return available_room_pretty



if __name__ == '__main__':
    week_now = "2"
    week_i_now = "1"
    course_i_now = "1234"
    print(query_room(week_now,week_i_now,course_i_now))


# 操场一
# 语言测试中心（实验北楼113）
# 实验B座506,508（一机房）
# 同声传译1（实验北楼108）
# 语言学习五室(实验北楼306)
# 办公楼450
# 实验B座606,608（五机房）
# 语言学习七室(实验北楼411)
# 3号公教楼B606

#print(query_room(week_now,week_i_now,course_i_now))


