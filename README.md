# qlu-cr
 查询校内空教室
> [demo 地址](https://qlu-cr.herokuapp.com/)

能力有限，欢迎issue和pull😊

- 如果要想要自己测试或更新.
> 
只需要如下两步：
1. 在```get_schedule.py```文件中修改开学时间（开学第一天）
```python
# <<<<<!!!定义开学时间!!!>>>>>
year,month,day=2022,8,23
```
2. 在 ```get_course_on_table.py```中提供在 [教务系统](http://jwxt-qlu-edu-cn.vpn.qlu.edu.cn/) 中的cookie，并且运行一次获得数据包
```python
# <<<<<!!!需要使用代理，提供Cookie获取数据!!!>>>>>
Cookie = "抓取提供"
```




如果对你有帮助的话，请star⭐一下

### 支持校区
- [x] 长清
- [ ] 菏泽
- [ ] 历城
- [ ] 彩石

  

  