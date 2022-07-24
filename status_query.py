import json
from login import login
import requests


def status_query(s, ip, detect_wan):
    adsl_status = s.post(f'http://{ip}/Action/call', json=detect_wan).text
    adsl_status = json.loads(adsl_status)

    ret = {}
    for i in adsl_status['Data']['iface_check']:
        ret[i['interface']] = i['errmsg']
    
    return ret


if __name__ == '__main__':
    ret = json.loads(open('ikuai.json', 'r').read())
    detect_wan = ret['detect_wan']

    s = requests.session()
    s.headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
        'Accept': 'application/json, text/plain, */*'
    }


    login(s, 'admin', 'a12345')

    print(status_query(s, detect_wan))