# 文件的更替
1.surface 与 笔记本同步(11.21.a.m）。删除css文件中的banner.css <br>
2.笔记本（11.22.a.m）。修改user_center.html和uer_center.css
3.surface（11.22.p.m)对views.py进行部分修改，主要对用户界面进行修改（未提交到GitHub）<br>
4.surface（11.23.p.m）添加路径（已提交)    
    path('user_center/del_good/', views.del_goods),<br>
    path('user_center/del_cart/', views.del_carts),<br>
    path('user_center/buy_allgood/', views.buy_goods),<br>
5.surface提交user_center.html和css <br>

# 待解决的问题

### 主界面
1.主界面的分类问题以及轮播图的链接问题（未解决）<br>

### 用户中心
1.需要在good_detail_page函数中判断id的值是否在数据库中，否则报错（未解决）<br>
2.在用户中心user_center界面中对用户发布的商品和购物车中的商品进行判断是否为空，然后进行提示（解决中）--只显示空白，不进行提示<br>
3.user_center界面中个人信息的展示和修改（未解决）<br>
4.购买商品的数据表<br>

# 已有的数据表
1.用户表(user)<br>
2.发布商品表(goods）<br>
3.分类表(sort)<br>
4.加入购物车商品表(cart)<br>
