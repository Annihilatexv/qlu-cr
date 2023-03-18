## qlu-cr
 查询校内空教室
> [demo 地址](https://cr.qlut.repl.co)


能力有限，欢迎issue和pull😊，如果对你有帮助的话，请帮忙star⭐一下

### Preview


![Preview.png](https://i.328888.xyz/2023/03/18/MkKKJ.png)


## 友链
- [nixiak](https://qlu.nixiak.xyz)


## 开发
**请勿部署或添加至任何商业项目中！**如果你部署了本项目，愿意给其他人**免费使用**，欢迎在仓库内留言添加友链！（或者发邮件至Annihilatexv@outlook.com）



如果要想要自己测试或更新
1. 配置 ```config/config.yaml``` 文件。
2. 运行一次```get_course_on_table.py```文件，来获取最新的课表数据。
3. 运行本项目。
4. 强烈建议创建定时任务，运行```get_course_on_table.py```定期更新课表数据


```yaml
#config/config.yaml

string :
  #使用自己的cookie
  Cookie : "Path=/; JSESSIONID=xxxxxxxxxxxxxxxxxxxxxxxxxxx"
  #### 有两种方式获取数据，二选其一

  # 1. 直连（推荐，需要在校园网局域网环境下）
  table_url : "http://jwxt.qlu.edu.cn/jsxsd/kbcx/kbxx_classroom_ifr"

  # 2. 使用VPN代理（不推荐，不需要校园网，但url可能会发生改变，届时需要自己抓取并替换前半域名）
  #table_url = "http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118/jsxsd/kbcx/kbxx_classroom_ifr"

list:
  # 开学那周的周一
  new_semester: [2023,2,20]
  # 考研时间
  exam_day: [2023,12,23]
  # 教室黑名单，根据关键字进行排除（长清->1，历城->3，菏泽->4）
  ban_list_1 : ['北楼', '语言', '办公', '3号', '同声', '机房', '同声传译', '实验北楼', '操场', '室','1号公教楼405','1号公教楼305','1号公教楼505','1号公教楼604']
  ban_list_3 : []
  ban_list_4 : []
```

- 不清楚其他校区情况，数据可能不准确 😫




## 参数获取
获取经 VPN 代理的```table_url```：[学校官网](https://www.qlu.edu.cn/)->[页面底部 VPN](https://vpn.qlu.edu.cn/)->教务管理
```text
http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118/jsxsd/kbcx/kbxx_classroom_ifr
将上述网址中的
http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118
替换为获取到的教务系统网址
```



### 支持校区
- [x] 长清
- [x] 菏泽
- [x] 历城
- [ ] 彩石

 


  