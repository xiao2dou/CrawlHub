from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('https://cn.bing.com/#')
browser.find_element_by_name('q').send_keys('rise')
browser.find_element_by_name('q').send_keys(Keys.ENTER)
