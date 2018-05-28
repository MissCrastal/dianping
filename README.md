# dianping
一个简单的爬大众点评美食相关商家和评论的程序

> 数据文件放在data目录下

#### 主程序：
1. get_users.py: 获取某件店的所有评论用户, user id会写入到user_list.csv文件中（不重复）
2. get_user_comments.py: 获取用户的评论，通过user_list.csv文件，添加到comments.csv文件
3. get_shops.py: 获取评论涉及到的店铺,添加到shop_list.csv文件中
4. get_shop_info.py: 获取店铺信息，添加到shop_info.csv文件
5. config.py: 配置文件
6. wait.py: 生成服从正态分布的程序停止时间

>note:每次运行时注意修改配置文件config.py下的参数和程序下的start参数
