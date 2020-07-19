from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('https://www.alexa.com/topsites/countries/CN')

tb=browser.find_element_by_xpath('//*[@id="alx-content"]/div/section/div[1]/section[2]/span/span/div/div/div[2]')
with open('domain.csv','w',encoding='utf-8-sig',newline='') as f:
    f.write(tb.text)

# 清洗爬取的数据，提取出域名
domain_list=[] 
with open('domain.csv','r',encoding='utf-8-sig',newline='') as f:
    i = 6
    for line in f.readlines():
        if(i%6==0):
            domain_list.append(line)
        i += 1

with open('domain.txt','w',encoding='utf-8-sig',newline='') as f:
    for item in domain_list:
        f.writelines(item)