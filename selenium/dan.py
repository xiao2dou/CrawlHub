from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('https://www.dan.me.uk/bgplookup')

count=6535#接着上一次继续跑的初值


while count<=64511:
    browser.find_element_by_name('asn').clear()
    browser.find_element_by_name('asn').send_keys(count)
    browser.find_element_by_name('asn').send_keys(Keys.ENTER)
    count+=1
    tb=browser.find_element_by_xpath('//*[@id="content-left-in"]/div/table')
    print(tb.text) #运行时重定向输出到文件python<dan.py>file.txt

