
import requests
#配置服务器ip地址
def return_ip():
    ip="http://192.168.109.110:5000/"
    return ip

# os.listdir(path)读取文件名时会自动多出一个Thumbs.db文件，去除函数
def del_surplus_file(filename_array):
    if 'Thumbs.db' in filename_array:
       filename_array.remove('Thumbs.db')
       return filename_array
    else:
        return filename_array

import hashlib  #md5加密函数
def md5(str):
    md5str=hashlib.md5(str.encode(encoding='utf-8')).hexdigest()
    return md5str

# print(md5('qxlEDP951039@163$adn'))#qxlEDP951039@163$+用户名admin第一二和最后一个字符



#封装计算两个点经纬度距离函数
from geopy.distance import geodesic as GD
def distance_calc(user_data,other_data):
    distance=GD(user_data,other_data)
    return distance

#封装比较距离最小的传的函数
def compare_min(*args):
    list_shop=list(args[0])   #传过来参数是元组，只有一个元素，转为列表
    # print('$$$$list_shop',list_shop)
    min_shopname=list_shop[0][0]
    min_data=list_shop[0][1]
    for i in list_shop:
        if i[1]<min_data:
            min_shopname=i[0]
    # print(min_shopname)

    return min_shopname

#封装微信小程序appid和AppSecret
def appid():
    ids='wx11312dda556c34cd'
    return ids
def appsecre():
    secre='05a66b157ba57f6c1a3f645b3872dbe0'
    return secre

#向微信服务器发送请求https://api.weixin.qq.com/sns/jscode2session，获取openid session_key
def get_openid_session_key( appid, code,secret):
        # print(appid,code,secret)
        url='https://api.weixin.qq.com/sns/jscode2session'
        parmas = {
            'appid': appid,
            'secret': secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        # Response=requests.post(url,datas)
        response=requests.get(url,params=parmas)
        # openid=Response.json().get('openid', '')  #获取openid


        return response




