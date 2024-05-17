import requests
import socket
import logging

# 校园网登录和注销相关URL（请根据实际情况设置正确的URL）
LOGIN_URL = "http://YOUR_LOGIN_URL"
UNBIND_URL = "http://YOUR_UNBIND_SERVER"
LOGOUT_URL = "http://YOUR_LOGOUT_SERVER"
CHECK_LOGOUT_URL = "http://YOUR_CHECK_LOGOUT_SERVER"

# 校园网登录的HTTP头部信息（请根据实际情况设置正确的User-Agent和Referer）
HEADERS = {
    "User-Agent": "YOUR_USER_AGENT",
    "Referer": "YOUR_REFERER"
}

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 从文件中读取登录凭证（请将下面的文件路径替换为实际存储登录凭证的文件路径）
def read_credentials():
    filename = "YOUR_CREDENTIALS_FILE_PATH"
    credentials = {}
    with open(filename, 'r') as file:
        credentials['user_account'] = file.readline().strip()
        credentials['user_password'] = file.readline().strip()
    return credentials

# 登录函数
def login_to_campus_network():
    # 初始化PARAMS字典
    PARAMS = {
        'callback': 'dr1004',
        'login_method': '1',
        'wlan_user_ip': socket.gethostbyname(socket.gethostname()),  # 获取本机IP地址
        'jsVersion': '4.2',
        'terminal_type': '1',
        'lang': 'zh-cn',
        'v': '10002'  
    }


    credentials = read_credentials()
    PARAMS.update(credentials)

    try:
        response = requests.get(LOGIN_URL, params=PARAMS, headers=HEADERS)
        if response.status_code == 200:
            if "Portal协议认证成功！" in response.text:
                logging.info("登录成功")
            else:
                logging.warning("登录失败，响应内容：" + response.text)
        else:
            logging.error("请求失败，状态码：" + str(response.status_code))
    except requests.RequestException as e:
        logging.error("请求过程中发生错误：" + str(e))

# 注销函数
def logout_from_campus_network():
    try:
        response = requests.get(UNBIND_URL, headers=HEADERS)
        if response.status_code == 200:
            logging.info("MAC地址解绑成功")
        else:
            logging.error("MAC地址解绑失败，状态码：" + str(response.status_code))

        response = requests.get(LOGOUT_URL, headers=HEADERS)
        if response.status_code == 200:
            logging.info("注销登录请求发送成功")
        else:
            logging.error("注销登录请求发送失败，状态码：" + str(response.status_code))

        response = requests.get(CHECK_LOGOUT_URL, headers=HEADERS)
        if response.status_code == 200:
            logging.info("注销确认请求发送成功")
        else:
            logging.error("注销确认请求发送失败，状态码：" + str(response.status_code))

    except requests.RequestException as e:
        logging.error("请求过程中发生错误：" + str(e))


# 主函数
def main():
    while True:
        action = input("请输入1进行登录，输入0进行注销，输入其他退出程序：")
        if action == '1':
            login_to_campus_network()  # 调用登录函数
        elif action == '0':
            logout_from_campus_network()  # 调用注销函数
        else:
            print("退出程序")
            break

if __name__ == "__main__":
    main()
