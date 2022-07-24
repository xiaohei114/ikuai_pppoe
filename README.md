# ikaui PPPOE


解决的问题：手上可以拨号的账号太多，不知道哪些可以用，可以使用此项目批量验证。  

说明：使用ikuai作为拨号基础和验证基础，因为win和linux没有好用的现成的拨号工具，用ikuai简单方便一点。  

使用：只需要修改`user_info.json`就可以了

ikuai_ip 就是 ikuai 的 ip 地址，  

user 里面的两个字段分别是登录 ikuai 的账户和密码，  

broadband 里面是需要拨号的宽带的账户和密码，account是账号，password是密码。



未来：

1. 优化数据结构，提高程序效率
2. 其他优化
   1. 账号读取
   2. 日志输出和保存
   3. 结果的输出和保存
3. 使用python拉起vbox虚拟机，实现完全自动化
4. 获取更多ikuai的api，提高此库的适用范围