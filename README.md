## qlu-cr

 查询校内空教室

> [demo 地址](https://cr.qlut.repl.co)

能力有限，欢迎issue和pull😊，如果对你有帮助的话，请帮忙star⭐一下

### Preview

![Preview.png](https://i.328888.xyz/2023/03/18/MkKKJ.png)

## 部署

**请勿部署或添加至任何商业项目中！**如果你部署了本项目，愿意给其他人**免费使用**，欢迎在仓库内留言添加友链！（或者发邮件至Annihilatexv@outlook.com）

### 1. 手动部署

1. 克隆本项目 ``git clone https://github.com/Annihilatexv/qlu-cr.git``。
2. 进入项目文件夹 ``cd qlu-cr``。
3. 配置 ``config/config.yaml`` 文件(参考下面)。
4. 运行一次 ``python get_course_on_table.py``，以获取最新的课表数据。
5. 运行本项目 ``gunicorn main:app -b 0.0.0.0:7694 -w 4``。
6. 访问 [ip:7694](http://127.0.0.1:7694)

#### ~~自动化更新~~(Cookie具有时效性，建议定期 ``python get_course_on_table.py``手动更新数据)

- ~~强烈建议创建定时任务，运行 ``python get_course_on_table.py``定期更新课表数据。~~

~~例如：~~

```
# 编辑crontab定时任务
crontab -e

#填入，并保存
0 5,12,17 * * * cd ~/qlu-cr && /usr/local/bin/python get_course_on_table.py >> /var/log/cron.log
# ~/qlu-cr为项目所在目录，/usr/local/bin/python为解释器目录，可以通过"which python"查询

# 查看定时任务
crontab -l
```

### 2. docker 部署

> ~~docker 版已集成自动更新课表数据~~

1. 下载并修改 [config.yaml](https://github.com/Annihilatexv/qlu-cr/blob/main/config/config.yaml)文件
2. 启动容器 (注意将“D:\Repositories\DockerStudy\config”替换为[config.yaml](https://github.com/Annihilatexv/qlu-cr/blob/main/config/config.yaml) 所在目录)

```sh
docker run -dp 7694:7694 --name qlu-cr -v D:\Repositories\DockerStudy\config:/app/config annihilatexv/qlu-cr:latest
```

3. 访问 [ip:7694](http://127.0.0.1:7694)

### 配置文件

```yaml
#config/config.yaml

string :
  #使用自己的cookie
  Cookie : "Path=/; JSESSIONID=xxxxxxxxxxxxxxxxxxxxxxxxxxx"
  #### 有两种方式获取数据，二选其一

  # 1. 直连（推荐，需要在校园网局域网环境下）
  table_url : "http://jwxt.qlu.edu.cn/jsxsd/kbcx/kbxx_classroom_ifr"

  # 2. 使用VPN代理（不推荐，不需要校园网，但url可能会发生改变，届时需要自己抓取并替换前半域名）
  #table_url : "http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118/jsxsd/kbcx/kbxx_classroom_ifr"

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

### 参数获取

1. Cookie 抓取直连/代理对应的[教务系统](http://jwxt.qlu.edu.cn/)Cookie 即可
2. 获取经 VPN 代理的 ``table_url``：[学校官网](https://www.qlu.edu.cn/)->[页面底部 VPN](https://vpn.qlu.edu.cn/)->教务管理

```text
http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118/jsxsd/kbcx/kbxx_classroom_ifr
将上述网址中的
http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn:8118
替换为获取到的教务系统网址
```

3. 所有教室名称可运行 `python get_course_on_table.py`查看

## 友链

- [nixiak](https://qlu.nixiak.xyz)

## 支持校区

- [X] 长清
- [X] 菏泽
- [X] 历城
- [ ] 彩石

- 空教室数据仅来自教务处，不包括社团、宣讲、考试等占用
