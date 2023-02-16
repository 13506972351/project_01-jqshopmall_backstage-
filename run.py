# _*_ coding:utf-8 _*_
from gevent import monkey
monkey.patch_all()
from gevent import pywsgi
from config import *
from config_tool import *
import math,json

from flask import Flask,url_for,render_template,redirect,request,jsonify
from datetime import datetime

import os
import socket

app=Flask(__name__)

app.config.from_object(__name__)   #为防止响应体中文在浏览器中乱码，在此调定json数据不以ascii格式返回
app.config["JSON_AS_ASCII"]=False

#####系统管理部份######
# login接口
@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['user']
        password=request.form['pass']

        if username and password:
            md5_pass_str=md5(password+username[0:2]+ username[len(username)-1:len(username)]) #原始密码加密
            res_pass=sys_select(username)  #数据库查询密码结果
            # print(res_pass,md5_pass_str)
            if res_pass==md5_pass_str:
                # print('===')
                return redirect(url_for('sys_manager',user_parameter=username,pass_parameter=password))

    return render_template('login.html')

# 后台管理系统主页接口
@app.route('/sys_manager',methods=['GET','POST'])
def sys_manager():

    use=request.args.get('user_parameter')
    pas=request.args.get('pass_parameter')
    # print(use,pas)
    md5_pass_str = md5(pas + use[0:2] + use[len(use)-1:len(use)])  # 原始密码加密
    res_pass = sys_select(use)  # 数据库查询密码结果
    if res_pass == md5_pass_str:
        return render_template('sys_manager.html')  #重定项
    else:
        return redirect(url_for('login'))

    return render_template('sys_manager.html')

# 后台管理系统新增shopname_list表数据请求接口
@app.route('/add_content',methods=['GET','POST'])
def add_content():
    datalist=[]
    province_str=request.form['province_str'],
    state_str= request.form['state_str'],
    county_str=request.form['county_str'],
    shopname_str=request.form['shopname_str'],
    master_str=request.form['master_str'],
    telep_str=request.form['telep_str'],
    pass_str=request.form['pass_str'],
    street_str=request.form['street_str']
    street_number_str=request.form['street_number_str']
    # print('shopname_str:',shopname_str)
    # print('shopname_str:',shopname_str,type(shopname_str),len(shopname_str))
    new_shopname = ''.join(shopname_str)  #将元组转为字符型(店铺名)
    new_pass_str = ''.join(pass_str)  # 将元组转为字符型（密码）
    # print(type(telep_str),len(telep_str))
    res = shop_list_select(new_shopname)  # 先查询是否存在
    # print('res:',res)
    if res:
        return 'T'  #已经重复，返回F给页面
    else:
        md5_pass_str = md5(new_pass_str+ new_shopname[0:2] + new_shopname[len(new_shopname) - 1:len(new_shopname)])
        # 原始密码+店铺名第一二最后一个字符
        add_res(province_str,state_str,county_str,shopname_str,master_str,telep_str,md5_pass_str,street_str,street_number_str)  #新增插入记录

        res=shop_list_select(new_shopname)   #新增完再查询
        # print('res::',res)
        if res:
            for i in res:
                newres=list(i)
                datalist.append(newres)
            # print('datalist',datalist)
            return datalist
        else:
            return 'F' #没找到新增的记录，返回F给页面
# 后台管理系统查询shopname_list表数据请求接口
@app.route('/select_content',methods=['GET','POST'])
def select_content():
    datalist=[]
    shopname_str=request.form['shopname_str'],
    # print('shopname_str:',shopname_str)
    new_shopname = ''.join(shopname_str)  #将元组转为字符型(店铺名)
    # print(type(telep_str),len(telep_str))
    res=shop_list_select(new_shopname)
    # print('res_select:',res)
    if res:
        for i in res:
            newres=list(i)
            datalist.append(newres)
        # print('datalist',datalist)
        return datalist
    else:
        return 'T'

# 后台管理系统删除shopname_list表数据请求接口
@app.route('/del_content',methods=['GET','POST'])
def del_content():
    shopname_str=request.form['shopname_str'],
    # print('shopname_str:',shopname_str)
    new_shopname = ''.join(shopname_str)  #将元组转为字符型(店铺名)
    # print(type(telep_str),len(telep_str))
    res=shop_list_select(new_shopname)
    if res:
        shop_list_del(new_shopname)
        res1 = shop_list_select(new_shopname)
        if res1:
            return 'B'
        else:
            return 'T'
    else:
        return 'F'

# 后台管理系统添加商品分类数据请求接口
@app.route('/add_goods_class',methods=['GET','POST'])
def add_goods_class():
    datalist = []
    goods_class_str = request.form['class_name']
    new_goods_class_str = ''.join(goods_class_str)  # 元组转为字符
    res = select_goodsclass(new_goods_class_str)  # 查询要添加的分类名
    if res:
        return 'T'
    else:
        add_goodsclass(goods_class_str)      #添加分类
        # print(goods_class_str)
        res1=select_goodsclass(new_goods_class_str)  #查询刚添加的分类名
        # print('new_goods_class_str',new_goods_class_str)
        # print('res:',res)
        if res1:
            for i in res1:
                newres = list(i)
                datalist.append(newres)
            # print('datalist:',datalist)
            return datalist
        else:
            return 'B'
# 后台管理系统查询商品分类数据请求接口
@app.route('/select_goods_class',methods=['GET','POST'])
def select_goods_class():
    datalist = []
    goods_class_str = request.form['select_str']
    # print(goods_class_str)
    res=select_goodsclass(goods_class_str)
    # print('RES:',res)
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        # print('datalist',datalist)
        return datalist
    else:
        return 'B'
# 后台管理系统删除商品分类数据请求接口
@app.route('/del_goods_class',methods=['GET','POST'])
def del_goods_class():
    goods_del_str = request.form['del_str']
    res = select_goodsclass(goods_del_str)
    if res:
        # print(goods_del_str)
        del_goodsclass(goods_del_str)
        res1 = select_goodsclass(goods_del_str)
        if res1:
            return 'B'
        else:
            return 'T'
    else:
        return 'F'

# 后台管理系统新增颜色接口
@app.route('/add_color',methods=['GET','POST'])
def add_color():
    datalist=[]
    color_name=request.form['color_name']
    color_id = request.form['color_id']
    # print(color_name,color_id)
    res=select_color_sql(color_id)
    # print('res:',res)
    if res:
        return 'T'
    else:
        add_color_sql(color_name,color_id)
        res1 = select_color_sql(color_id)
        if res1:
            for i in res1:
                newres = list(i)
                datalist.append(newres)
            # print('datalist:',datalist)
            return datalist
        else:
            return 'B'
# 后台管理系统查询颜色接口
@app.route('/select_color',methods=['GET','POST'])
def select_color():
    datalist=[]
    color_name=request.form['color_name']  #查询以颜色名为查询条件
    # print(color_name,color_id)
    res=select_color_sql(color_name)
    # print('res:',res)
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return 'B'
# 后台管理系统删除颜色接口
@app.route('/del_color',methods=['GET','POST'])
def del_color():
    datalist=[]
    color_id = request.form['color_id']
    # print(color_name,color_id)
    res=select_color_sql(color_id)
    # print('res:',res)
    if res:
        del_color_sql(color_id)
        res1 = select_color_sql(color_id)
        if res1:
            return 'B'
        else:
            return 'T'
    else:
        return 'F'
# 后台管理系统新增尺码接口
@app.route('/add_size',methods=['GET','POST'])
def add_size():
    datalist=[]
    size_name=request.form['size_name']
    size_id = request.form['size_id']
    # print(size_name,size_id)
    res=select_size_sql(size_id)
    print('res:',res)
    if res:
        return 'T'
    else:
        add_size_sql(size_name,size_id)
        res1 = select_size_sql(size_id)
        if res1:
            for i in res1:
                newres = list(i)
                datalist.append(newres)
            # print('datalist:',datalist)
            return datalist
        else:
            return 'B'
# 后台管理系统查询尺码接口
@app.route('/select_size',methods=['GET','POST'])
def select_size():
    datalist=[]
    size_name=request.form['size_names']  #查询以尺码名为查询条件
    # print(size_name)
    res=select_size_sql(size_name)
    # print('res:',res)
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return 'B'
# 后台管理系统删除尺码接口
@app.route('/del_size',methods=['GET','POST'])
def del_size():
    datalist=[]
    size_id = request.form['size_id']
    # print(size_name,size_id)
    res=select_size_sql(size_id)
    # print('res:',res)
    if res:
        del_size_sql(size_id)
        res1 = select_size_sql(size_id)
        if res1:
            return 'B'
        else:
            return 'T'
    else:
        return 'F'

#后台管理系统商品管理页面，初始化加载商品分类信息
@app.route('/load_goodsclass',methods=['GET','POST'])
def load_goodsclass():
    datalist = []
    sql_str=1
    res=select_goodsclass(sql_str)
    # print(res)
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        return datalist
    else:
        return 'B'

# 后台管理系统商品管理页面，初始化加载尺码信息
@app.route('/load_size',methods=['GET','POST'])
def load_size():
    datalist = []
    sql_str = 1
    res = select_size_sql(sql_str)
    # print(res)
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        return datalist
    else:
        return 'B'

#后台管理系统商品管理页面，新增商品信息接口
@app.route('/add_goods_list',methods=['GET','POST'])
def add_goods_list():
    datalist=[]
    goods_number=request.form['goods_number']
    goods_class=request.form['goods_class']
    goods_describe=request.form['goods_describe']
    original_Price=request.form['original_Price']
    colorid_str=request.form['colorid_str']
    colorname_str=request.form['colorname_str']
    sizeid_str=request.form['sizeid_str']
    sizename_str=request.form['sizename_str']
    img_url=request.form['img_url']
    goods_state=request.form['goods_state']
    #判断是否有相同款号和颜色id的记录，如果有，不让重复添加
    res1 = select_goods_information(goods_number)   #先查询是否有相同款号的记录
    config=True
    if res1:
        for i in res1:
            if i[5]==colorid_str:
                config=False
    if config:
        add_goods_information(goods_number, goods_class, goods_describe, original_Price, colorid_str,
                              colorname_str, sizeid_str, sizename_str, img_url, goods_state)
        res = select_goods_information(goods_number)
        if res:
            for i in res:
                newres = list(i)
                datalist.append(newres)
            # print('datalist:',datalist)
            return datalist
        else:
            return 'B'  #不成功
    else:
        return 'R'  # 返回R代表有重复

#后台管理系统商品管理页面，查询商品信息接口
@app.route('/select_goods_list',methods=['GET','POST'])
def select_goods_list(*args):
    datalist=[]
    goods_number=request.form['goods_number']
    # print(goods_number)
    res=select_goods_information(goods_number)
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return 'B'

#后台管理系统商品管理页面，删除商品信息接口
@app.route('/del_goods_list',methods=['GET','POST'])
def del_goods_list():
    goods_number=request.form['goods_number']
    res=select_goods_information(goods_number)
    if res:
        del_goods_information(goods_number)
        res1 = select_goods_information(goods_number)
        if res1:
            return 'B'
        else:
            return 'T'#成功无返回
    else:
        return 'N'   #记录不存在

##后台管理系统商品管理页面，修改商品信息接口
@app.route('/modify_goods_list',methods=['GET','POST'])
def modify_goods_list():
    goods_number = request.form['goods_number']
    goods_class = request.form['goods_class']
    goods_describe = request.form['goods_describe']
    original_Price = request.form['original_Price']
    colorid_str = request.form['colorid_str']
    colorname_str = request.form['colorname_str']
    sizeid_str = request.form['sizeid_str']
    sizename_str = request.form['sizename_str']
    img_url = request.form['img_url']
    goods_state = request.form['goods_state']

    # 提前将数据库中有，但是修改表单里没有的颜色记录删除
    color_id_arrstr=request.form.getlist('color_id_arrstr[]')  #提前将所有颜色id提交给接口做判断（ajxa发送数组加上getlist('变量名[]')）
    # print('color_id_arrstr:',color_id_arrstr)
    s=1
    if s==1:
        s=s+1
        res=select_goods_information(goods_number)  #查询同款记录
        if res:
            for i in res:
                if i[5] not in color_id_arrstr:
                    del_goods_information(i[0])

    res1 =select_goods_information_many(goods_number,colorid_str)  # 查询同款同颜色id记录
    # print('res:',res)
    if res1:   #如果同款同色记录存在，则修改记录
        ids=res1[0][0]  #获取id，以此作为修改条件
        # print(ids)
        modify_goods_information(goods_number,goods_class,goods_describe,original_Price,colorid_str,colorname_str,sizeid_str,sizename_str,img_url,goods_state,ids)
        # return 'T'
    else:   #如果同款同色记录不存在
        add_goods_information(goods_number, goods_class, goods_describe, original_Price, colorid_str,
                              colorname_str, sizeid_str, sizename_str, img_url, goods_state)

    res2 = select_goods_information(goods_number)  # 再次查询记录
    datalist = []
    if res2:
        for i in res2:
            newres = list(i)
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return 'B'

#####用户管理部份######
#用户管理系统，后台登录
@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        shop_name = request.form['shop_name']
        pass_word=request.form['pass']
        # print(shop_name,pass_word)
        if shop_name and pass_word:
            md5_pass_str=md5(pass_word+shop_name[0:2]+ shop_name[len(shop_name)-1:len(shop_name)]) #原始密码加密
            res_pass=user_loin_select(shop_name)  #数据库查询用户密码结果
            if res_pass==md5_pass_str:
                return redirect(url_for('user_manager',user_parameter=shop_name,pass_parameter=pass_word))   #此处待加盐
    return render_template('user_login.html')

#用户管理系统，后台主页面
@app.route('/user_manager',methods=['GET','POST'])
def user_manager():
    shop = request.args.get('user_parameter')
    pas = request.args.get('pass_parameter')
    # print(use,pas)
    md5_pass_str = md5(pas + shop[0:2] + shop[len(shop) - 1:len(shop)])  # 原始密码加密
    res_pass = user_loin_select(shop)  # 数据库查询密码结果
    if res_pass == md5_pass_str:
        return render_template('user_manager.html')  # 重定项
    else:
        return redirect(url_for('user_login'))

    return render_template('user_manager.html')

#用户管理系统，加载商品信息到用户管理界面(查询款号)
@app.route('/select_goods_number',methods=['GET','POST'])
def select_goods_number():
    datalist=[]
    res=select_goods_number_info()
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return 'B'

#用户管理系统，加载商品信息到用户管理界面(查询用户选取记录)
@app.route('/select_user_goods_list',methods=['GET','POST'])
def select_user_goods_list(*args):
    datalist=[]
    user_shop_name=request.form['user_shop_name']
    goods_number=request.form['goods_number']
    # print(goods_number)
    res=select_user_shop_goods_information(user_shop_name,goods_number)
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return ''


#用户管理系统，向用户商品信息表添加商品记录
@app.route('/add_user_goods_list',methods=['GET','POST'])
def add_user_goods_list():
    g_number=request.form['goods_name']
    g_class=request.form['goods_class']
    color_id=request.form['color_id']
    color_name=request.form['color_name']
    size_id=request.form['size_id']
    size_name=request.form['size_name']
    sale_price=request.form['sale_price']
    shop_name=request.form['shop_name']
    original_price=request.form['original_price']
    img_url=request.form['img_url']
    g_describe=request.form['goods_describe']

    add_user_goods_information(g_number,g_class,color_id,color_name,size_id,size_name,sale_price,shop_name,original_price,img_url,g_describe)
    res=select_user_shop_goods_information(shop_name,g_number)
    # res=select_user_shop_goods_information()
    # print(g_number,g_class,color_id,color_name,size_id,size_name,sale_price,shop_name,original_price,img_url,g_describe)
    datalist = []
    if res:
        for i in res:
            newres = list(i)
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return ''

#用户管理系统，删除用户商品信息表商品记录
@app.route('/del_user_goods_list',methods=['get','post'])
def del_user_goods_list():
    shop_name=request.form['user_shop_name']
    # print(shop_name)
    del_user_goods_information(shop_name)
    return ''
#测试接口
@app.route('/cs',methods=['get','post'])
def cs():
    # fileName = request.getParameter("fileName")
    # print(fileName)
    return redirect(url_for('user_manager'))


#********************微信小程序管理部份*********************
#定义一个变量，用于存储服务器Ip地址

ipurl_str=return_ip()   #调用服务器ip地址配置函数
#返回轮播图地址数组
@app.route('/load_swiper_img',methods=['GET','POST'])
def load_swiper_img():
    datalist = []
    res=load_swiper_imgurl('swiper')
    if res:
        # print(res)
        for i in res:
            # print(list(i))
            res_list=list(i)
            newres=[ipurl_str + x for x in res_list]   #给个数组元素前面加上ip字符
            datalist.append(newres)
        # print('datalist:',datalist)
        return datalist
    else:
        return ''

#处理小程序送来的用户位置，计算距离最近的店铺
@app.route('/calc_lately_location',methods=['GET','POST'])
def calc_lately_location():
    #小程序提交来的用户所在省地市街道信息
    province=request.form['provinces'].strip('"')   #.strip('"')去除字符中的“
    city=request.form['citys'].strip('"')
    district = request.form['districts'].strip('"')
    street= request.form['streets'].strip('"')
    street_number = request.form['street_numbers'].strip('"')

    # print(latitude_str)
    # print(province,city,district,street,street_number)
    location_info=[]
    if len(province)>0 and len(city)>0 and len(district)>0 and len(street)>0 and len(street_number)>0:
        location_info.append(province)
        location_info.append(city)
        location_info.append(district)
        location_info.append(street)
        location_info.append(street_number)


    tup_location_info=tuple(location_info)  #将列表转为元组
    # print(location_info,tup_location_info)
    shop_name=''
    shops_list=[]
    for i in range(len(tup_location_info),0,-1):  #用元组个数从大到小循环找出同一地点的店铺
        str=tup_location_info[0:i]
        # print('*',str)
        res=calc_lately_shop(*str)    #将元组作为参数传给函数，函数用*args,会多一个外围的括号，此时在传参时在参数前加个*，作为函数拆包,返回店铺名
        if res:
            # print('res',res)
            for i in res:    #由于满足条件的店铺不止一个，遍历所有满足条件的店名，找出有添加商品的店铺
                # print('i',i)
                res1 = select_useroods_list(i)  # 查询该店铺有没有添加user_goods_list商品资料
                if res1:
                    # print('res1=',res1[0][8])   #因为res1为该店商品信息，不止一条，选第一条的店铺名称
                    shop_name=res1[0][8]
                    # print('shop_name:',shop_name)
                    break
        else:
            continue
    # print('shop_name=',shop_name)
    if shop_name!='':
        return shop_name


    elif shop_name=='':
        res1 = calc_lately_shop_Field(province)   #查询外省所有店铺的地址：(省+市*店铺名)，返回给前端
        # print("res1====",res1)
        if res1:
            return res1
    else:
        return 'B'


#计算外省离用户最近的店铺
@app.route('/calc_lately_Field_shop',methods=['GET','POST'])
def calc_lately_Field_shop():
    user_latitude = request.form['latitude_strs']  # 用户纬度
    user_longitude = request.form['longitude_strs']  # 用户经度
    shop_address_info = request.form['shop_add_info'].strip('"')   #.strip('"')去除字符中的“
    shop_address_info=shop_address_info[0:len(shop_address_info)-1]   #去除最后一个*
    shop_address_info=shop_address_info.split('*')   #以*为准分割列表
    # print('&&&&&',shop_address_info)
    new_shop_add_list=[]
    for i in shop_address_info:  #循环各店名经纬度大列表
        new_group={}
        grouping=i.split(',')     #将单店名经纬度分割成小列表
        # print(grouping)
        for s in range(0,len(grouping)-1):
            # print(grouping[0],grouping[1],grouping[2])
            new_group[grouping[0]]={'lais':eval(grouping[1]),'lngs':eval(grouping[2])}
    #         new_group['name']=  str(grouping[0])
    #         new_group['lais'] = eval(grouping[1])
    #         new_group['lngs'] = eval(grouping[2])
        new_shop_add_list.append(new_group)   #分别添加到新的大列表中
        # print(new_group)

    user_data = (user_latitude, user_longitude)   #将用户经纬度放入元组
    list_shop_distance=[]
    for i in new_shop_add_list:  #遍历店铺单元
        # print('i',i.keys())
        lai_lng_list=[]
        for s in i.values():      #遍历店铺内经纬度值
            # print('s',s)
            for y in s.values():   #遍历单店经度值和纬度值
                # print('y',y)
                lai_lng_list.append(y)   #将经度和纬度两次添加到列表中
            tup_lai_lng_list=tuple(lai_lng_list)   #转元组
            #调用两个经纬度距离函数
            distance=distance_calc(user_data,tup_lai_lng_list)
            strs=str(distance)    #转字符
            num=eval(strs[0:len(strs) - 3]) #去掉单位km，再转数字

        name=list(i.keys())  #key转列表
        name.append(num)    #添加距离值
        list_shop_distance.append(name)  #添加到大列表中
    # print('*',list_shop_distance,len(list_shop_distance))

    res=compare_min(list_shop_distance)
    # print('^^^res',res)
    if res:
        return res
    else:
        return 'B'

#返回中央主视区图片接口
@app.route('/central_vision_img_get',methods=['GET','POST'])
def central_vision_img_get():
    lately_shop_name = request.form['lately_shop_name']  # 最近店铺名

    new_datalist=[]
    # print('**',lately_shop_name)
    res=select_central_vision_img(lately_shop_name)
    if res:
        for i in res:
            datalist = {}
            datalist['goods_number']=(i[0])
            datalist['goods_describe'] = (i[1])
            datalist['goods_original'] = (i[2])
            datalist['goods_sale'] = (i[3])
            datalist['goods_url'] = (ipurl_str+i[4])
            datalist['shop_name'] = (i[5])
            datalist['shop_class']=(i[6])
            # list_res = list(i)
            # print('777',datalist)

            new_datalist.append(datalist)
        # print('new_datalist:',new_datalist)
        return list(new_datalist)
    else:
        return ''

#点击主视区商品分类，查询商品图片，渲染主视区
@app.route('/appoint_goodsclass_central_vision_img_get',methods=['GET','POST'])
def appoint_goodsclass_central_vision_img_get():
    lately_shop_name = request.form['lately_shop_name']  # 最近店铺名
    appoint_goodsclass_name=request.form['appoint_goods_class']    #指定商品分类
    new_datalist=[]
    # print('**',lately_shop_name,appoint_goodsclass_name)
    res=appoint_goodsclass_select_central_vision_img(lately_shop_name,appoint_goodsclass_name)
    # print(res)
    if res:
        for i in res:
            datalist = {}
            datalist['goods_number']=(i[0])
            datalist['goods_describe'] = (i[1])
            datalist['goods_original'] = (i[2])
            datalist['goods_sale'] = (i[3])
            datalist['goods_url'] = (ipurl_str+i[4])
            datalist['shop_name'] = (i[5])
            datalist['shop_class']=(i[6])
            # list_res = list(i)
            # print('777',datalist)

            new_datalist.append(datalist)
        # print('new_datalist:',new_datalist)
        return list(new_datalist)
    else:
        return ''
#商品祥情页面获取图片及商品资料接口
@app.route('/load_goods_specific',methods=['GET','POST'])
def load_goods_specific():
    goods_number=request.form['goods_name']
    shop_name=request.form['shop_name']
    res=load_goods_specific_info(goods_number,shop_name)
    res1=shop_list_select(shop_name)
    # print('res1',res1)
    new_datalist = []
    if res:
        for i in res:
            datalist = {}
            datalist['goods_number']=(i[1])
            datalist['goods_class']=(i[2])
            datalist['color_id'] = (i[3])
            datalist['color_name'] = (i[4])
            datalist['size_id'] = (i[5])
            datalist['size_name'] = (i[6])
            datalist['sale_price'] = (i[7])
            datalist['shop_name'] = (i[8])
            datalist['original_price'] = (i[9])
            datalist['img_url'] = (ipurl_str + i[10])
            datalist['goods_describe'] = (i[11])
            datalist['shop_add']=(res1[0][3]+res1[0][4])

            # list_res = list(i)
            # print('777',datalist)
            new_datalist.append(datalist)
        # print('new_datalist:',new_datalist)
        return list(new_datalist)
    else:
        return ''
    # print('---',res)
    return ''

#微信用户登录接口
@app.route('/wx_user_login',methods=['GET','POST'])
def wx_user_login():
    lately_shop_name=request.form['shop_name']
    code_str=request.form['code_str']
    app_id=appid()   #调用配置函数，
    app_secres=appsecre()

    res=get_openid_session_key(app_id, code_str, app_secres)  #调用获取openid和session_key接口
    if res:

        openid = res.json().get('openid', '')  # 获取openid
        session_key=res.json().get('session_key','')  # 获取session_key
        key=md5(openid)  #调用md5加密session_key
        dt01 = datetime.today()  #获取当前日期
        dates=dt01.date()
        write_vip_info(lately_shop_name,dates,openid,key)  #写入数据库


        return key
    else:
        return 'B'




if __name__=='__main__':   #原生写法，单线程效率低
    app.run(host='0.0.0.0',debug=True,    #外网或局域网访问必须设置host='0.0.0.0'
            port=5000)
#
# if __name__ == '__main__':
#     server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
#     server.serve_forever()