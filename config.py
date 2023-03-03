#coding=utf-8
import pymysql
import traceback
# 将数据库操作封装成类
class mysqlhelp:
    def __init__(self,host='127.0.0.1',port=3306,user='root',password='admin123',database='shopmall_jq',charset='utf8'):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.database=database
        self.charset=charset
    def open_conn(self):    #打开数据库连接和游标
        self.conn=pymysql.connect(host=self.host,port=self.port,user=self.user,password=self.password,database=self.database,charset=self.charset)
        self.cursor=self.conn.cursor()
    def close_conn(self):  #关闭数据库连接和游标
        self.cursor.close()
        self.conn.close()
    def add_del_upd(self,sql,params=[]):  #增加删除修改params为参数（元组）
        try:
            self.open_conn()  #打开
            self.cursor.execute(sql,params)
            self.conn.commit()
            self.close_conn() #关闭

            print('成功')
            return 'T'
        except Exception as e:
            self.conn.rollback()
            print(e)

    def select_all(self,sql,params=[]):  #查询
        try:
            self.open_conn()
            self.cursor.execute(sql,params)
            res=self.cursor.fetchall()
            self.close_conn()
            return res
        except Exception as e:
            print(e)

######系统管理部份######
# sys管理系统用户登录验证
def sys_select(sqlstr):
    sql_str='select pass from sys_master where username=%s'
    params = [sqlstr, ]
    conn = mysqlhelp()
    # print(conn)
    res = conn.select_all(sql_str, params)
    if (res):
        newres=list(res)[0][0]
        return newres
    else:
        return False

# 添加店铺列表~~~~~~~~~~~~~~~
def add_res(province_str,state_str,county_str,shopname_str,master_str,telep_str,pass_str,street_str,street_number_str):
    sql_str= "INSERT INTO shop_list (`shop_name`,`shop_master`,`province`,`state`,`county`,`pass`,`Tel`,`street`,`street_number`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    params=[shopname_str,master_str,province_str,state_str,county_str,pass_str,telep_str,street_str,street_number_str]
    conn = mysqlhelp()
    conn.add_del_upd(sql_str, params)

# 查询店铺列表~~~~~~~~~~~~~~~
def shop_list_select(sqlstr):
    sql_str = 'select id,shop_name,shop_master,province,state,county,street,street_number,tel from shop_list where shop_name=%s'
    params = [sqlstr, ]
    conn = mysqlhelp()
    # print(conn)
    res = conn.select_all(sql_str, params)
    # print('res:::', res)
    if (res):
        return res
    else:
        return

# 删除店铺列表~~~~~~~~~~~~~~~
def shop_list_del(sqlstr):
    sql_str = 'delete from shop_list where shop_name=%s'
    params = [sqlstr, ]
    conn = mysqlhelp()
    conn.add_del_upd(sql_str, params)

# 添加商品分类表~~~~~~~~~~~~~~~
def add_goodsclass(class_str):
    sql_str="INSERT INTO goods_class (`class_name`)  VALUES (%s)"
    params = [class_str, ]
    conn = mysqlhelp()
    # print(conn)
    conn.add_del_upd(sql_str, params)

# 查询商品分类表~~~~~~~~~~~~~~~
def select_goodsclass(sqlstr):
    trace = traceback.extract_stack()[-2][2]  # 返回函数调用者信息,
    # print('返回函数调用者:',trace)
    if trace=="load_goodsclass":  #如果是点击商品管理按钮，加载所有商品分类信息时
        sql_str = 'select class_name from goods_class where 1=%s'
    else:
        sql_str = 'select * from goods_class where class_name=%s'  #正常查询
    params = [sqlstr, ]
    conn = mysqlhelp()
    # print('dd',sqlstr)
    res = conn.select_all(sql_str, params)
    # print('res::',res)
    if (res):
        return res
        # print('res::', res)
    else:
        return  #记录不存在返回none

# 删除商品分类表~~~~~~~~~~~~~~~
def del_goodsclass(sqlstr):
    # print('sqlstr:',sqlstr)
    sql_str='delete from goods_class where class_name=%s'
    params=[sqlstr,]
    conn=mysqlhelp()
    conn.add_del_upd(sql_str,params)

#新增颜色
def add_color_sql(sqlstrA,sqlstrB):
    sql_str = "INSERT INTO color_table (`name`,`color_id`)  VALUES (%s,%s)"
    params = [sqlstrA,sqlstrB]
    conn = mysqlhelp()
    # print(conn)
    conn.add_del_upd(sql_str, params)
#查询颜色
def select_color_sql(sqlstr):
    trace=traceback.extract_stack()[-2][2]   #返回函数调用者信息
    # print('返回函数调用者:',trace)
    if trace=='select_color': #查询按钮以颜色名为条件，新增按钮以颜色id为条件
        sql_str="select * from color_table where name=%s"
    elif trace=='load_color':
        sql_str = "select color_id,name from color_table where 1=%s"  #加载颜色复选框
    else:
        sql_str="select * from color_table where color_id=%s"
    params = [sqlstr, ]
    conn = mysqlhelp()
    # print('dd',sqlstr)
    res = conn.select_all(sql_str, params)
    # print('res::',res)
    if (res):
        return res
        # print('res::', res)
    else:
        return  # 记录不存在返回none
#删除颜色
def del_color_sql(sqlstr):
    # print('sqlstr:',sqlstr)
    sql_str='delete from color_table where color_id=%s'
    params=[sqlstr,]
    conn=mysqlhelp()
    conn.add_del_upd(sql_str,params)
#新增尺码
def add_size_sql(sqlstrA,sqlstrB):
    sql_str = "INSERT INTO size_table (`name`,`size_id`)  VALUES (%s,%s)"
    params = [sqlstrA,sqlstrB]
    conn = mysqlhelp()
    # print(conn)
    conn.add_del_upd(sql_str, params)
#查询尺码
def select_size_sql(sqlstr):
    trace=traceback.extract_stack()[-2][2]   #返回函数调用者信息
    # print('返回函数调用者:',trace)
    if trace=='select_size': #查询按钮以尺码名为条件，新增按钮以尺码id为条件
        sql_str="select * from size_table where name=%s"
    elif trace=='load_size':
        sql_str="select size_id,name from size_table where 1=%s"
    else:
        sql_str="select * from size_table where size_id=%s"
    params = [sqlstr, ]
    conn = mysqlhelp()
    # print('dd',sqlstr)
    res = conn.select_all(sql_str, params)
    # print('res::',res)
    if (res):
        return res
        # print('res::', res)
    else:
        return  # 记录不存在返回none
#删除尺码
def del_size_sql(sqlstr):
    # print('sqlstr:',sqlstr)
    sql_str='delete from size_table where size_id=%s'
    params=[sqlstr,]
    conn=mysqlhelp()
    conn.add_del_upd(sql_str,params)

#新增商品信息
def add_goods_information(goods_number,goods_class,goods_describe,Price,colorid,colorname,sizeid,sizename,img_url,goods_state):
    sql_str = "INSERT INTO goods_list (`goods_number`,`goods_class`,`goods_describe`,`original_price`,`color_id`,`color_name`,`size_id`,`size_name`,`img_url`,`goods_state`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    params = [goods_number,goods_class,goods_describe,Price,colorid,colorname,sizeid,sizename,img_url,goods_state]
    conn = mysqlhelp()
    # print(conn)
    conn.add_del_upd(sql_str, params)

#查询商品信息（单条件）
def select_goods_information(*args):    #*args为不确定参数个数
    sql_str = "select * from goods_list where goods_number=%s"
    params = args       #如果用*args作为参数，args本身是元组不需要加[args,]中括号及逗号
    conn = mysqlhelp()
    # print(args)
    res = conn.select_all(sql_str, params)
    # print('res::',res)
    if (res):
        return res
        # print('res::', res)
    else:
        return  # 记录不存在返回none

#查询商品信息（多条件）
def select_goods_information_many(*args):    #*args为不确定参数个数
    sql_str="select * from goods_list where goods_number=%s and color_id=%s"
    params = args       #如果用*args作为参数，args本身是元组不需要加[args,]中括号及逗号
    conn = mysqlhelp()
    # print(args)
    res = conn.select_all(sql_str, params)
    # print('res::',res)
    if (res):
        return res
        # print('res::', res)
    else:
        return  # 记录不存在返回none

#删除商品信息
def del_goods_information(sqlstr):
    trace=traceback.extract_stack()[-2][2]
    if trace=='modify_goods_list':
        sql_str = 'delete from goods_list where id=%s'
    else:
        sql_str = 'delete from goods_list where goods_number=%s'
    params = [sqlstr, ]
    conn = mysqlhelp()
    conn.add_del_upd(sql_str, params)

#修改商品信息
def modify_goods_information(*args):
    sql_str='update goods_list set goods_number=%s,goods_class=%s,goods_describe=%s,original_price=%s,color_id=%s,color_name=%s,size_id=%s,size_name=%s,img_url=%s,goods_state=%s where id=%s;'
    params = args
    conn = mysqlhelp()
    conn.add_del_upd(sql_str, params)

######用户管理部份######
#查询用户密码
def user_loin_select(*args):
    sql_str = "select pass from shop_list where shop_name=%s"
    params = args  # 如果用*args作为参数，args本身是元组不需要加[args,]中括号及逗号
    conn = mysqlhelp()
    # print(args)
    res = conn.select_all(sql_str, params)
    # print('res::',res)
    if (res):
        newres = list(res)[0][0]
        return newres
        # print('res::', res)
    else:
        return  # 记录不存在返回none

#查询所有商品信息（款号唯一值,禁用的和轮播图分类的除外）
def select_goods_number_info(*args):
    sql_str = "select distinct goods_number from goods_list where goods_state=1 and goods_class!='swiper'"

    params = args  # 如果用*args作为参数，args本身是元组不需要加[args,]中括号及逗号
    conn = mysqlhelp()
    # print(args)
    res = conn.select_all(sql_str, params)
    # print('res::',res)
    if (res):
        # newres = list(res)[0][0]
        return res
        # print('res::', res)
    else:
        return  # 记录不存在返回none

#查询指定店铺已选取商品信息表
def select_user_shop_goods_information(*args):
    sql_str='select *  from user_goods_list where shop_name=%s and goods_number=%s'
    params=args
    conn=mysqlhelp()
    res=conn.select_all(sql_str,params)
    if(res):
        return res
    else:
        return



#新增用户商品信息记录
def add_user_goods_information(*args):
    sql_str = "INSERT INTO user_goods_list (`goods_number`,`goods_class`,`color_id`,`color_name`,`size_id`,`size_name`,`sale_price`,`shop_name`,`original_price`,`img_url`,`goods_describe`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # sql_str = "INSERT INTO user_goods_list  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    params = args
    conn = mysqlhelp()
    # print(conn)
    conn.add_del_upd(sql_str, params)

#删除用户商品信息记录
def del_user_goods_information(*args):
    sql_str="delete from user_goods_list where shop_name=%s"
    params=args
    conn=mysqlhelp()
    conn.add_del_upd(sql_str,params)

# res=select_goods_info()
# print(res)

#********************微信小程序管理部份*********************
# 查询轮播图url
def load_swiper_imgurl(*args):
    sql_str = 'select img_url  from goods_list where goods_class=%s'
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if (res):
        # print(res)
        return res
    else:
        return

# 查询用户本省距离最的店铺
def calc_lately_shop(*args):
    s=len(args)
    # print(s,args)
    if s==5:
        sql_str = 'select shop_name from shop_list where province=%s and state=%s and county=%s and street=%s and street_number=%s'
    elif s==4:
        sql_str = 'select shop_name from shop_list where province=%s and state=%s and county=%s and street=%s'
    elif s==3:
        sql_str = 'select shop_name from shop_list where province=%s and state=%s and county=%s'
    elif s==2:
        sql_str = 'select shop_name from shop_list where province=%s and state=%s'
    elif s==1:
        sql_str = 'select shop_name from shop_list where province=%s'

    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if (res):
        # print('result:',res)
        return res
    else:
        return

# 查询外省距离最的店铺
def calc_lately_shop_Field(*args):
    res_list=[]
    new_res_list=[]
    sql_str = 'select province,state,shop_name from shop_list where province!=%s'
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if (res):
        # print('result:',res)

        for i in range(len(res)):
            # print('res[i][2]',res[i][2])
            res2 = select_useroods_list(res[i][2])  # 查询该店铺有没有添加user_goods_list商品资料
            # print('res2',res2)
            if res2:
                # print('*i=',i)
                newres=res[i][0]+res[i][1]+'*'+res[i][2]
                # print(newres)
                # print('i',i)
                res_list.append(newres)
                # print(res_list)
                new_res_list=list(set(res_list))   #set删除列表中的重复元素,返回的是字典，再转化为列表
        # print(new_res_list)
        return new_res_list

    else:
        return


#查询最近店铺是否有添加商品到店商品管理表中，如果没有，会选择另一家近的店铺
def select_useroods_list(*args):
    sql_str = 'select * from user_goods_list where shop_name=%s'
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if (res):
        # print('result:',res)
        return res
    else:
        return

#查询主视区图片地址
def select_central_vision_img(*args):
    sql_str = 'select distinct goods_number,goods_describe,original_price,sale_price,img_url,shop_name,goods_class from user_goods_list where shop_name=%s '
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if (res):
        # print('result:',res)
        return res
    else:
        return

#点击主视区商品分类，查询商品图片，渲染主视区
def appoint_goodsclass_select_central_vision_img(*args):
    sql_str = 'select distinct goods_number,goods_describe,original_price,sale_price,img_url,shop_name,goods_class from user_goods_list where shop_name=%s  and goods_class=%s'
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if (res):
        # print('result:',res)
        return res
    else:
        return

#查询商品祥情信息
def load_goods_specific_info(*args):
    sql_str = 'select * from user_goods_list where goods_number=%s and shop_name=%s'
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if (res):
        # print('result:',res)
        return res
    else:
        return

#查询是否有相同的openid，即是否已经注册过了
def select_openid(*args):
    sql_str="select * from vip_table where openid=%s"
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if res:
        return res
    else:
        return

#向vip_table写入相关信息
def write_vip_info(*args):
    # print('ddd', lately_shop_name, dates, openid, key, nick, sex, tel, add)
    sql_str = "INSERT INTO vip_table (`ascription_shop`,`register_date`,`openid`,`login_key`,`nick_name`,`sex`,`telethone`,`rec_add`)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

    params = args
    conn = mysqlhelp()
    # print(conn)
    conn.add_del_upd(sql_str, params)

#微信用户查询是否已经注册过
def select_keys(*args):
    sql_str = "select * from vip_table where login_key=%s"
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    if res:
        return res
    else:
        return

#查询微信小程序用户购物车信息
def select_shop_car(*args):
    sql_str = "select * from shop_car where login_key=%s"
    params = args
    conn = mysqlhelp()
    res = conn.select_all(sql_str, params)
    print(res)
    if res:
        return res
    else:
        return