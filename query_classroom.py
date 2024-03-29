import joblib
from get_course_on_table import multidict,load_dict



# 查找空教室
def query_room(week_now,week_i_now,course_i_now,ban_list,district=1):
    all_week = 7
    day_course = 6
    available_room=[]


    # 加载已保存的课表
    all_classroom = joblib.load(r'./static/data/all_classroom_{}.pkl'.format(district))
    course_on_table = load_dict("./static/data/course_on_table_{}.json".format(district))

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
    available_room_filtered = []

    for room in available_room:
        for ban in ban_list:
            if ban in room:
                break
        else:
            available_room_filtered.append(room)

    # 过滤后是否有可用教室
    if available_room_filtered:
        available_room_pretty = pretty(available_room_filtered)
    else:
        available_room_pretty=['运气爆棚！没有可用的教室，hahaha!']

    return available_room_pretty


# 美化空教室输出（maybe）
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
    print(query_room(week_now = "2",week_i_now = "1",ban_list=[],course_i_now = "1234",district=1))


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


