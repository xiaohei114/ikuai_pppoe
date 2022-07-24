import requests
import logging
import json

from login import login

def inquire_pppoe(s, ip, inquire_wan):
    """查询 [基于物理网卡的拨号]"""
    ret = s.post(url=f'http://{ip}/Action/call', json=inquire_wan)

    if ret.status_code != 200:
        logging.error('请求错误，状态码非200, 返回状态码:{0}'.format(ret.status_code))
        exit()
    
    ret = json.loads(ret.text)


    vlan_name_list, mac_list, user_name_list = [], [], []

    for i in ret['Data']['vlan_data']:
        vlan_name_list.append(i['vlan_name'])
        mac_list.append(i['mac'])
        user_name_list.append(i['username'])
        # print(i['vlan_name'])
        # print(i['mac'])
        # print(i['username'])
        # print(i['passwd'])
    
    return {
        'vlan_name': vlan_name_list,
        'mac': mac_list,
        'user_name': user_name_list
    }


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    s = requests.session()
    s.headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
        'Accept': 'application/json, text/plain, */*'
    }

    login(s, 'admin', 'a12345')

    data = json.loads(open('ikuai.json', 'r').read())
    data = data['inquire_wan']
    data = inquire_pppoe(s, data)

    print(data)
