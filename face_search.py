import time
import baidu_face

if __name__ == '__main__':
    file_path = '/Users/zhangwenchao/Downloads/登记10w/登记20180718/3/15ab4e7780484076803b010e60b26ae8.jpg'
    s = time.time()
    print(baidu_face.face_search(file_path))
    # baidu_face.bulk_face_search()
    print('花费时间：', time.time() - s)
