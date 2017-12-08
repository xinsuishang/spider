import os
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import *


browser = webdriver.Chrome(service_args=SERVICE_ARGS)
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 5)
browser.set_window_size(1400, 900)
path = os.path.join(ROOT, FILE_NAME)

def register(identity, time=5):
    if time == 0:
        browser.close()
        browser.set_window_size(1400, 900)
        return None
    try:
        browser.get(URL)
        print('URL打开成功')
        try:
            logOut = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#aleardylogin > div > div > div.rr > a.btn-user-logout.logOut'))
            )
            logOut.click()
            print('已注销')
        except:
            pass
        reg = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#launch-register')))
        reg.click()
        print('点击注册成功')
        logEmail = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#logEmail'))
        )
        logEmail.send_keys(identity)
        print('输入要注册的账号完成')
        logPwd = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#logPwd'))
        )
        logPwd.send_keys(identity)
        print('输入密码完成')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#register > form > div.surePasswordDiv.input.logindiv > input'))
        )
        input.send_keys(identity)
        print('再次输入密码完成')
        # protocol = wait.until(
            # EC.element_selection_state_to_be((By.CSS_SELECTOR,'#regProtocol'), True)
        # )
        protocol = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#regProtocol'))
        )
        # protocol = wait.until(
            # EC.element_to_be_selected(protocol, True)
        # )
        protocol.click()
        print('已同意协议')
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#nowRegister'))
        )
        submit.click()
        print('register success!')
        save_to_text(identity)
    except TimeoutException:
        time -= 1
        register(identity, time)

def random_str():
    return ''.join(random.choice(RD_STR) for i in range(12))

def mkdir():
    if os.path.exists(ROOT):
        return None
    os.mkdir(ROOT)

def save_to_text(identity):
    with open(path, 'a') as f:
        identity += '\n'
        f.write(identity)

def main():
    mkdir()
    for i in range(300):
        register(random_str())
    browser.close()

if __name__ == '__main__':
    main()
