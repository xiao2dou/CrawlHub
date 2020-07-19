from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.find_element_by_id('kw').send_keys('php')
browser.find_element_by_id('kw').send_keys(Keys.ENTER)
