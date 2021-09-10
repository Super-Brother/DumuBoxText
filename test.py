from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
}
url = 'http://www.baidu.com'


def test(i):
    print('第{}次访问'.format(i))
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        return 'OK'
    else:
        return 'Failure'


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as executor:
        task_list = [executor.submit(test, i) for i in range(100)]
        for item in as_completed(task_list):
            print(item.result())
