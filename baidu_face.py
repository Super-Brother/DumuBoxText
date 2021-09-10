import concurrent.futures
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import base64
import requests

headers = {
    'Authorization': 'Bearer b8dd29b53c1a955572823010b09ecd82',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
}
base_url = 'http://192.168.100.57:8080'
# 注册人像
url = base_url + '/staffManage/addStaffInfo'
# 1:N人像对比
url_face_1vn = base_url + '/faceAnalysis/faceSearch'
path_list = [
    '/Users/zhangwenchao/Downloads/登记10w/登记20180718/1',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180718/2',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180718/3',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180719-21/1',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180719-21/2',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180719-21/3',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180719-21/4',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180719-21/5',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180719-21/6',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180719-21/7',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180722-24/1',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180729-31',
    '/Users/zhangwenchao/Downloads/登记10w/登记20180803-05',
]

# 使用会话，免去了TCP/IP的握手
session = requests.session()
session.headers = headers


# 图片转base64
def fileToBase64(file_path):
    # 1、文件读取
    ext = file_path.split(".")[-1]
    with open(file_path, 'rb') as fileObj:
        image_data = fileObj.read()
    # 2、base64编码
    base64_data = base64.b64encode(image_data).decode()
    # 3、图片编码字符串拼接
    src = "data:image/{ext};base64,{data}".format(ext=ext, data=base64_data)
    return src


# 插入人像
def insertFace(file_path):
    base64_data = fileToBase64(file_path)

    body = {
        'staff_pool': 'test2',
        'staff_name': '111',
        'face_image': base64_data,
    }

    html = session.post(url, headers=headers, json=body)
    if html.status_code == 200:
        html.encoding = 'utf8'
        json = html.json()
        return json
    else:
        return '插入人像失败! error_code={}'.format(html.status_code)


# 批量插入人像
def bulkInsert():
    s = time.time()
    file_list = []
    for path in path_list:
        files = os.listdir(path)
        for file in files:
            file_list.append(path + "/" + file)
    print("图片总数:", len(file_list))
    with ThreadPoolExecutor(max_workers=2) as executor:
        task_list = [executor.submit(insertFace, file_path) for file_path in file_list]
        for item in concurrent.futures.as_completed(task_list):
            print(item.result())
    print('花费时间：', time.time() - s)


# 1vN对比
def face_search(file_path):
    base64_data = fileToBase64(file_path)

    body = {
        'staff_pools': ['test1'],
        'source_img': base64_data,
        'threshold': 80,
    }

    html = session.post(url_face_1vn, headers=headers, json=body)
    if html.status_code == 200:
        html.encoding = 'utf8'
        json = html.json()
        return json
    else:
        return '1vn人像对比失败! error_code={}'.format(html.status_code)


# 1vN并发测试
def bulk_face_search():
    s = time.time()
    file_list = []
    for path in path_list:
        files = os.listdir(path)
        for file in files:
            file_list.append(path + "/" + file)
    print("图片总数:", len(file_list))
    with ThreadPoolExecutor(max_workers=32) as executor:
        task_list = [executor.submit(face_search, file_path) for file_path in file_list]
        for item in concurrent.futures.as_completed(task_list):
            print(item.result())
    print('花费时间：', time.time() - s)
