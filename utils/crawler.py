# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re


def chrome_no_gui():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="E:/PycharmProjects/qaautotest/driver/Windows/chromedriver.exe",
                              options=chrome_options)
    return driver


def get_element_source(element):
    element_source = element.get_attribute("innerHTML")
    return element_source


def get_img_url(html_source):
    p1 = "https://.[^\s]+?.jpg|https://.[^\s]+?.png"
    pattern = re.compile(p1)
    img_list = pattern.findall(html_source)
    return img_list


def is_exist(url):
    response = requests.get(url=url)
    state_code = response.status_code
    if state_code == 200:
        print("%s: 正常打开" % url)
    else:
        print("%s: 404" % url)


if __name__ == '__main__':
    # url = "https://h5test.elab-plus.com/adver/index.html#/pages/haiheTech"
    # web_driver = chrome_no_gui()
    # web_driver.get(url)
    # web_driver.implicitly_wait(10)
    # app = web_driver.find_element_by_xpath('//*[@id="app"]')
    # ele_source = get_element_source(app)
    # img_list = get_img_url(ele_source)
    # for img in img_list:
    #     is_exist(img)
    is_exist("https://dm.static.elab-plus.com/haiheTech/item_dweweweees_7.png")
