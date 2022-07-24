import base64
import hashlib
import logging
import json
import requests


def b64(s):
    # 对传入字符串做base64编码
    ss = s.encode('utf-8')  # 返回字节数组bytes
    return base64.b64encode(ss)  # 参数支持bytes

def password(s):
    # 生成密码base64
    return b64('salt11_'+s).decode('utf-8')


def passwd(s):
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def login(s, ip, user_name, user_pass):
    login_info = {
        'pass': password(user_pass),
        'passwd': passwd(user_pass),
        'remember_password': "",
        'username': user_name
    }

    logging.info("开始登录")
    logging.debug("请求参数: {0}".format(login_info))
    
    ret = s.post(f'http://{ip}/Action/login', json=login_info).text
    
    try:
        
        ret = json.loads(ret)
        result, errmsg = str(ret['Result']), str(ret['ErrMsg'])
        logging.debug("返回状态: {0} {1}".format(result, errmsg))

        if result == '10000' and errmsg == 'Succeess':
            logging.info("登录成功")
        else:
            logging.error("登录失败! 即将退出程序.")
            exit()
    except BaseException as e:
        print(e)
        exit()


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
    login(s, '192.168.2.250', 'admin', 'a12345')