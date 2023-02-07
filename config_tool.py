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

def ip_str(ipstr):
    return ipstr

#封装计算两个点经纬度距离函数
from geopy.distance import geodesic as GD
def distance_calc(user_data,other_data):
    distance=GD(user_data,other_data)
    return distance

#封装比较距离最小的传的函数
def compare_min(*args):
    return ''