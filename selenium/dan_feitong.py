# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


def change_ip(): # 更换vps的ip地址，应对反爬虫
    print("start change ip")
    os.system("pppoe-stop")
    time.sleep(1)
    os.system("pppoe-start")
    ip = os.popen("curl ip.3322.net").read()
    ip = ip.strip()
    if not ip:
        print("change ip fail, change again")
        change_ip()
    print("IP already change: "+ip)


if __name__ == '__main__':
    count = 6535  # 接着上一次继续跑的初值
    while True: # 死循环，失败了就创新新的文件，继续写入
        f_out = open(str(count)+'.txt', 'a+')
        option = webdriver.ChromeOptions()
        option.add_argument('--no-sandbox')
        option.add_argument('--headless')
        browser = webdriver.Chrome(executable_path='/twitter/chromedriver', options=option)
        try:
            browser.get('https://www.dan.me.uk/bgplookup')

            while count<=64511:
                browser.find_element_by_name('asn').clear()
                browser.find_element_by_name('asn').send_keys(count)
                browser.find_element_by_name('asn').send_keys(Keys.ENTER)
                count+=1
                tb=browser.find_element_by_xpath('//*[@id="content-left-in"]/div/table')
                print(tb.text) #运行时重定向输出到文件python<dan.py>file.txt
                f_out.write(tb.text+'\n')
        except Exception as e:
            print(e)
            change_ip()
            browser.quit()
            f_out.close()
            continue
