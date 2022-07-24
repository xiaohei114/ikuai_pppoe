import random
import json
import logging
import requests

from login import login

def random_mac():
    mac = [
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def generate_name(vlan_name_list):
    index = 1
    while True:
        test = f'adsl{str(index)}'
        if test not in vlan_name_list:
            return test
        else:
            index += 1

def add_pppoe(s, vlan_name, usernaem, passwd, mac):
    ret = json.loads(open('ikuai.json', 'r').read())
    add_adsl = ret['add_adal']
    print(add_adsl)

    add_adsl['param']['vlan_name'] = vlan_name
    add_adsl['param']['username'] = usernaem
    add_adsl['param']['passwd'] = passwd
    add_adsl['param']['mac'] = mac

    ret = s.post(url='http://192.168.2.250/Action/call', json=add_adsl)

    if ret.status_code != 200:
        logging.error('请求错误，状态码非200, 返回状态码:{0}'.format(ret.status_code))
        exit()
    
    ret = json.loads(ret.text)

    print(ret)

# def add_pppoe():
#     ret = json.loads(open('ikuai.json', 'r').read())
#     add_adsl = ret['add_adal']
#     print(add_adsl)
    

if __name__ == '__main__':
    data = ['adsl1', 'adsl2', 'adsl3', 'adsl4']
    # print(generate_name(data))

    print(random_mac())

    s = requests.session()

    login(s, 'admin', 'a1235')

    add_pppoe(s, generate_name(data), 'test', 'test', random_mac())