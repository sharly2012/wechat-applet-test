#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- coding: gb18030 -*-


import time
from appium import webdriver
from utils.baseoperate import BaseOperate

desired_caps = {
    'platformName': "Android",
    'platformVersion': "8.0.0",
    'deviceName': "b7556c74",
    'appPackage': "com.tencent.mm",
    'appActivity': ".ui.LauncherUI",
    'unicodeKeyboard': False,
    'resetKeyboard': False,
    'noReset': True,
    'chromeOptions': {'androidProcess': 'com.tencent.mm:appbrand0'}
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
base_operate = BaseOperate(driver)
base_operate.sleep(8)
m, n = base_operate.get_screen_size()
print(m, n)
driver.find_element_by_xpath("//*[@resource-id='com.tencent.mm:id/bq']/android.widget.LinearLayout[1]/android.widget.RelativeLayout[3]").click()
base_operate.sleep(2)
base_operate.swipe_up()
driver.find_element_by_xpath("//*[@text='小程序']").click()
base_operate.sleep(2)
base_operate.tap(int(995 / 1080 * base_operate.width), int(145 / 1920 * base_operate.height))
time.sleep(3)
driver.find_element_by_xpath("//*[@text='搜索小程序']").click()
driver.find_element_by_xpath("//*[@text='搜索小程序']").send_keys("济南高新金茂墅")
time.sleep(2)
base_operate.tap(int(540 / 1080 * base_operate.width), int(286 / 1920 * base_operate.height))
time.sleep(5)
base_operate.tap(int(540 / 1080 * base_operate.width), int(286 / 1920 * base_operate.height))
time.sleep(10)
try:
    if "下一步" in driver.page_source:
        base_operate.tap(int(540 / 1920 * base_operate.width), int(1110 / 2244 * base_operate.height))
        time.sleep(1)
        base_operate.tap(int(286 / 1920 * base_operate.width), int(2028 / 2244 * base_operate.height))
        time.sleep(1)
    else:
        pass
except:
    pass

image_path = "E:/PycharmProjects/wechat-applet-automation/screenshots/test"
for i in range(6):
    base_operate.get_screenshot(image_path, "homepage")
    base_operate.wechat_swipe_up()
    time.sleep(1)
driver.close_app()
