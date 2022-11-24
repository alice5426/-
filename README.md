# 文件的更替

1.surface 与 笔记本同步(11.21 a.m）。删除css文件中的banner.css <br>
2.笔记本（11.22 a.m）。修改user_center.html和uer_center.css
3.surface（11.22 p.m)对views.py进行部分修改，主要对用户界面进行修改（未提交到GitHub）<br>
4.surface（11.23 p.m）添加路径（已提交)    
    path('user_center/del_good/', views.del_goods),<br>
    path('user_center/del_cart/', views.del_carts),<br>
    path('user_center/buy_allgood/', views.buy_goods),<br>
5.surface提交user_center.html和css <br>
### surface任务
11.24 p.m 对用户中心的个人信息进行修改，达到对用户的头像等信息进行存在判断，并显示在个人信息栏当中。用户也可以对信息进行修改，保存后存储到用户数据表当中。

记录：

surface:  

1.添加"user_center/user_information/"，路径以及users_information()函数，进行用户信息的传输.  
2.user表中添加字段（img（varchar）、birthday（date）、address（varchar））  
3.user_center()函数中添加变量user，获取当前用户的相关信息。(已提交） 

笔记本：

1.添加购买的物品的表Buy

# 待解决的问题

### 一、主界面

1.主界面的分类问题以及轮播图的链接问题（未解决）<br>
2.关于商品展示页面URL中的id检测  
3.需要在good_detail_page函数中判断id的值是否在数据库中，否则报错（未解决）<br>

### 二、用户中心

1.在用户中心user_center界面中对用户发布的商品和购物车中的商品进行判断是否为空，然后进行提示（解决中）--只显示空白，不进行提示<br>
2.user_center界面中个人信息的展示和修改（未解决）<br>
3.购买商品的数据表（未解决）<br>

### 三、路径问题

1.设置最开始界面路径（未解决）  
2.关于路径的隐私问题（为考虑）  


# 已有的数据表

1.用户表(user)<br>
2.发布商品表(goods）<br>
3.分类表(sort)<br>
4.加入购物车商品表(cart)<br>

# 需要的防御手段

1.csrf  
2.SQL  
3.xss（可以适当考虑），暂时存在xss的为用户中心中的反馈界面，按常规来说反馈的数据会展示在admin的主界面当中，但是由于admin的主界面并没有设置，所以xss还不会显示出来。  
