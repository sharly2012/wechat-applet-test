#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author: sharly

import time
from appium import webdriver
from utils.baseutil import BaseUtil


class BaseDriver:
    def __init__(self):
        self.platformName = BaseUtil().get_yaml_value("DEVICES", "platformName")
        self.platformVersion = BaseUtil().get_yaml_value("DEVICES", "platformVersion")
        self.deviceName = BaseUtil().get_yaml_value("DEVICES", "deviceName")
        self.browserName = BaseUtil().get_yaml_value("DEVICES", "browserName")
        self.app = BaseUtil().get_yaml_value("DEVICES", "app")
        self.appPackage = BaseUtil().get_yaml_value("DEVICES", "appPackage")
        self.appActivity = BaseUtil().get_yaml_value("DEVICES", "appActivity")
        self.automationName = BaseUtil().get_yaml_value("DEVICES", "automationName")
        self.unicodeKeyboard = BaseUtil().get_yaml_value("DEVICES", "unicodeKeyboard")
        self.resetKeyboard = BaseUtil().get_yaml_value("DEVICES", "resetKeyboard")
        self.newCommandTimeout = BaseUtil().get_yaml_value("DEVICES", "newCommandTimeout")
        self.noReset = BaseUtil().get_yaml_value("DEVICES", "noReset")
        self.chromeOptions = BaseUtil().get_yaml_value("DEVICES", "chromeOptions")

    def applet_driver(self):
        desired_caps = {
            'platformName': self.platformName,
            'platformVersion': self.platformVersion,
            'deviceName': self.deviceName,
            'appPackage': self.appPackage,
            'appActivity': self.appActivity,
            'noReset': self.noReset,
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'chromeOptions': self.chromeOptions

        }
        applet_drive = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        time.sleep(5)
        applet_drive.activate_ime_engine("io.appium.settings/.UnicodeIME")
        return applet_drive

    def app_driver(self):
        desired_caps = {
            'platformName': self.platformName,
            'platformVersion': self.platformVersion,
            'deviceName': self.deviceName,
            'appPackage': self.appPackage,
            'appActivity': self.appActivity,
            'unicodeKeyboard': True,
            'resetKeyboard': True,
            'noReset': self.noReset
        }

        app_driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        time.sleep(5)
        app_driver.activate_ime_engine("io.appium.settings/.UnicodeIME")
        return app_driver
