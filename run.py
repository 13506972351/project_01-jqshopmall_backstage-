# _*_ coding:utf-8 _*_
from gevent import monkey
monkey.patch_all()
from gevent import pywsgi
from config import *
from config_tool import *
import math,json

from flask import Flask,url_for,render_template,redirect,request,jsonify

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
        add_res(province_str,state_str,county_str,shopname_str,master_str,telep_str,md5_pass_str)  #新增插入记录

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
    # res=select_user_shop_goods_information()
    # print(g_number,g_class,color_id,color_name,size_id,size_name,sale_price,shop_name,original_price,img_url,g_describe)
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

if __name__=='__main__':   #原生写法，单线程效率低
    app.run(host='0.0.0.0',debug=True,    #外网或局域网访问必须设置host='0.0.0.0'
            port=5000)
#
# if __name__ == '__main__':
#     server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
#     server.serve_forever()