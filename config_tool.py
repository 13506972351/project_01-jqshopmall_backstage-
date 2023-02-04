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