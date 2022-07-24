import requests
import json
import logging
import time


from login import login
from inquire_pppoe import inquire_pppoe
from status_query import status_query
from adsl import random_mac, generate_name, add_pppoe


def check(data, err_message):
    if data is None or data == '':
        logging.error(err_message)
        exit()


class Ikuai:
    def __init__(self) -> None:
        # logging.getLogger().setLevel(logging.DEBUG)  # 设置日志等级
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

        '关闭requests输出, 参考: https://learnku.com/python/t/23046/python-ignores-the-log-of-the-requests-library-when-using-the-logging-library'
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)


        self.ip = None
        self.username = None
        self.password = None
        self.broadband = None
        self._info_check()

        self.tracking = []  # 对列表内的宽带进行状态跟踪

        logging.debug(f"需要拨号的宽带 {self.broadband}")


        self.ret = json.loads(open('ikuai.json', 'r').read())


        # 创建并设置会话
        self.s = requests.session()
        self.s.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'
        }

        login(self.s, self.ip, self.username, self.password)

        self.used_adsl = inquire_pppoe(self.s, self.ip, self.ret['inquire_wan'])
        logging.debug(f'目前已有的拨号设备: {self.used_adsl}')

        self.add_adsl()

        # print(status_query(self.s, self.ret['detect_wan']))
        # print('\n\n\n\n', self.used_adsl['user_name'])
        data = self.status_query()
        for i in zip(self.used_adsl['vlan_name'], self.used_adsl['user_name']):
            if i[0] in data.keys():
                # print(i)
                print(f'接口: {i[0]}, 账户: {i[1]}, {data[i[0]]}')




    def _info_check(self):
        """读取信息并做校验"""
        # 信息读取
        tmp = json.loads(open('user_info.json', 'r').read())
        self.ip, user, self.broadband = tmp['ikuai_ip'], tmp['user'], tmp['broadband']

        # ip验证
        check(self.ip, "ip不能为空")

        # ikuai登录信息验证
        self.username, self.password = user['username'], user['password']
        check(self.username, "ikuai登录用户名不能为空！")
        check(self.password, "ikuai登录密码不能为空！")

        # 宽带信息验证
        dials_number = len(self.broadband)  # 需要拨号的宽带数量
        for i in self.broadband:  # 如果账号或者密码为空, 认定为填写错误, 不需要拨号
            if ((i['account']  is None or i['account']  == '') or \
                (i['password'] is None or i['password'] == '')):
                dials_number -= 1
                self.broadband.remove(i)
        if dials_number <= 0:
            logging.error("没有需要拨号的宽带")
            exit()
    
    def add_adsl(self):
        for i in self.broadband:
            adsl = self.ret['add_adal']
            # print(self.used_adsl['vlan_name'])
            adsl['param']['vlan_name'] = generate_name(self.used_adsl['vlan_name'])
            adsl['param']['username'] = i['account']
            adsl['param']['passwd'] = i['password']
            adsl['param']['mac'] = random_mac()

            self.used_adsl['vlan_name'].append(adsl['param']['vlan_name'])
            self.used_adsl['user_name'].append(adsl['param']['username'])
            self.used_adsl['mac'].append(adsl['param']['mac'])

            self.tracking.append(adsl['param']['vlan_name'])

            ret = self.s.post(url=f'http://{self.ip}/Action/call', json=adsl)

            if ret.status_code != 200:
                logging.error('请求错误，状态码非200, 返回状态码:{0}'.format(ret.status_code))
                exit()
            
            # ret = json.loads(ret.text)
            # print(ret)
    
    def status_query(self):
        count = 0
        while True:
            adsl_status = self.s.post(f'http://{self.ip}/Action/call', json=self.ret['detect_wan']).text
            adsl_status = json.loads(adsl_status)

            # print(self.tracking)

            ret = {}

            for i in adsl_status['Data']['iface_check']:
                if i['interface'] in self.tracking:
                    ret[i['interface']] = i['errmsg']
                    # print(i['interface'])
                else:
                    # logging.warning(i['interface'])
                    pass

            t = [False for x in ret.keys() if x in self.tracking]
            if len(t) == len(self.tracking):
                break

            count +=1
            if count >= 100:
                logging.error(f"尝试 {count} 次后，无法获取到指定接口的拨号结果")
                exit()
            else:
                logging.debug("等待ikuai返回拨号结果中……")
                
            
            time.sleep(1)
            
        # print(ret)
        return ret


ikaui = Ikuai()

