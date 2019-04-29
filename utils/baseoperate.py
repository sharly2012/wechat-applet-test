#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- coding: gb18030 -*-

# @author: sharly

import inspect
import time
import allure
import pytesseract
import os
import math
import operator
import shutil
from functools import reduce
from unittest import TestCase
from PIL import Image
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import By
from utils.logger import Logger

logger = Logger(logger='BaseOperate').get_log()


class BaseOperate(object):

    def __init__(self, driver):
        """init"""
        self.driver = driver
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']
        self.timeout_time = 15
        self.wait_time = 2
        cur_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.split(cur_path)[0]

    def reset(self):
        """reset driver"""
        logger.info("reset the driver ...")
        self.width = self.driver.get_window_size()['width']
        self.height = self.driver.get_window_size()['height']
        return self

    def find_element(self, *locator):
        """find the element"""
        try:
            WebDriverWait(self.driver, 10, 0.5).until(lambda driver: driver.find_element(*locator).is_displayed())
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            logger.error('Can not find element: %s' % locator[1])
            raise
        except TimeoutException:
            logger.error('Can not find element: %s' % locator[1])

    def find_elements(self, by, value):
        """find elements"""
        try:
            if by == "id":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_id(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_element_by_id(value)
                return elements
            if by == "name":
                find_name = "//*[@text='%s']" % value
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_xpath(find_name).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_element_by_xpath(find_name)
                return elements
            if by == "xpath":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_xpath(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_element_by_xpath(value)
                return elements
            if by == "class_name":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_class_name(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_element_by_class_name(value)
                return elements
            if by == "content":
                WebDriverWait(self.driver, self.timeout_time).until(
                    lambda driver: driver.find_element_by_accessibility_id(value).is_displayed())
                self.driver.implicitly_wait(self.wait_time)
                elements = self.driver.find_element_by_accessibility_id(value)
                return elements
            else:
                raise NameError("Please Enter correct elements value")
        except NoSuchElementException:
            logger.warning("Can not find elements: %s" % value)
            raise

    def click(self, locator):
        """click"""
        logger.info('Click element by %s: %s ...' % (locator[0], locator[1]))
        try:
            ele = self.find_element(*locator)
            ele.click()
        except AttributeError as e:
            logger.error("The element is unclickable: %s" % e)

    def clear_input(self, locator):
        """clear the input"""
        element = self.find_element(*locator)
        try:
            element.clear()
            logger.info('Clear input-box by %s: %s ...' % (locator[0], locator[1]))
        except NameError as ne:
            logger.warning("Failed to clear in input box with %s" % ne)

    def send_keys(self, locator, text):
        """send keys"""
        ele = self.find_element(*locator)
        ele.clear()
        logger.info('Input element by %s : %s values %s ...' % (locator[0], locator[1], text))
        try:
            ele.send_keys(text)
        except Exception as e:
            logger.error("Failed to type in input box with %s" % e)

    def tap(self, x, y):
        """tap element"""
        logger.info("Tap positions x: %s, y: %s ..." % (x, y))
        try:
            TouchAction(self.driver).tap(x=x, y=y).perform()
        except Exception as e:
            logger.info(e)

    def long_tap(self, x=0, y=0, wait_time=1):
        """long tap element"""
        logger.info("Tap positions x: %s, y: %s ..." % (x, y))
        action = TouchAction(self.driver)
        action.long_press(None, x, y).perform()
        time.sleep(wait_time)
        action.release().perform()

    def sleep(self, sleep_time):
        """sleep"""
        logger.info("sleep %s seconds" % sleep_time)
        return time.sleep(sleep_time)

    def get_element_text(self, locator):
        """get the element text"""
        try:
            element = self.find_element(*locator)
            return element.text
        except Exception as e:
            logger.info("Can't get the text of %s" % locator)
            logger.error(e)

    def get_screen_size(self):
        """get the mobile screen size"""
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipe_up(self, duration=600, swipe_times=1):
        """swipe up"""
        logger.info("slide up the screen ...")
        size = self.get_screen_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.75)
        y2 = int(size[1] * 0.25)
        for i in range(swipe_times):
            self.driver.swipe(x1, y1, x1, y2, duration)

    def swipe_down(self, duration=600, swipe_times=1):
        """swipe down"""
        logger.info("slide down the screen ...")
        size = self.get_screen_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.25)
        y2 = int(size[1] * 0.75)
        for i in range(swipe_times):
            self.driver.swipe(x1, y1, x1, y2, duration)

    def swipe_left(self, duration=600, swipe_times=1):
        """swipe left"""
        logger.info("slide left the screen ...")
        size = self.get_screen_size()
        x1 = int(size[0] * 0.75)
        y1 = int(size[1] * 0.5)
        x2 = int(size[0] * 0.25)
        for i in range(swipe_times):
            self.driver.swipe(x1, y1, x2, y1, duration)

    def swipe_right(self, duration=600, swipe_times=1):
        """swipe right"""
        logger.info("slide right the screen ...")
        size = self.get_screen_size()
        x1 = int(size[0] * 0.25)
        y1 = int(size[1] * 0.5)
        x2 = int(size[0] * 0.75)
        for i in range(swipe_times):
            self.driver.swipe(x1, y1, x2, y1, duration)

    def wechat_swipe_up(self, duration=1000):
        """wechat applet slide up"""
        logger.info("wechat slide up")
        size = self.get_screen_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.75)
        y2 = int(size[1] * 0.25)
        action = TouchAction(self.driver)
        action.press(x=x1, y=y1).wait(ms=duration).move_to(x=x1, y=y2).wait(ms=duration).release()
        action.perform()

    def wechat_swipe_down(self, duration=800):
        """wechat applet slide down"""
        logger.info("wechat slide down")
        size = self.get_screen_size()
        x1 = int(size[0] * 0.5)
        y1 = int(size[1] * 0.25)
        y2 = int(size[1] * 0.75)
        action = TouchAction(self.driver)
        action.press(x=x1, y=y1).wait(ms=duration).move_to(x=x1, y=y2).wait(ms=duration).release()
        action.perform()

    def scroll_element1_to_element2(self, locator1, locator2):
        ele1 = self.find_element(*locator1)
        ele2 = self.find_element(*locator2)
        logger.info("scroll the screen from %s to %s" % (ele1, ele2))
        self.driver.scroll(ele1, ele2)

    def click_back(self):
        """click the back button, KEYCODE_BACK = 4"""
        logger.info("click the back button ...")
        self.driver.press_keycode(4)
        self.sleep(1)

    def click_home(self):
        """click the home button, KEYCODE_HOME = 3"""
        logger.info("click the home button ...")
        self.driver.press_keycode(3)

    def click_power(self):
        """click the power button, KEYCODE_POWER = 26"""
        logger.info("click the power button ...")
        self.driver.press_keycode(26)

    def click_search(self):
        """click the power button, KEYCODE_POWER = 84"""
        logger.info("click the search button ...")
        self.driver.press_keycode(84)

    def is_displayed(self, locator):
        """verify the element is or not exist"""
        try:
            element = self.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException as e:
            logger.info("Not exist this element %s" % e)

    def is_exist_current(self, text):
        """verify the text is or not in the page source"""
        all_element = self.driver.page_source
        if text in all_element:
            return True
        else:
            logger.info("Current page not exist %s" % text)
            return False

    def long_press(self, locator, duration=3000):
        """long press"""
        logger.info("long press % s" % locator)
        element = self.find_element(*locator)
        touch_action = TouchAction(self.driver)
        touch_action.long_press(element, duration).perform()

    def hide_keyboard(self):
        """hide the keyboard"""
        logger.info("hide the keyboard ...")
        self.driver.hide_keyboard()

    def get_screenshot(self, folder_name, case_name):
        """screen shot"""
        file_name = self.get_current_time() + '_' + case_name
        file_path = '%s/%s.png' % (folder_name, file_name)
        self.driver.get_screenshot_as_file(file_path)
        allure.attach.file(file_path, attachment_type=allure.attachment_type.PNG)
        logger.info("Screen shot had been saved: %s" % file_path)
        return file_path

    def launch_app(self):
        """launch the app"""
        logger.info("launch the app ...")
        self.driver.launch_app()

    def close_app(self):
        """close the app"""
        logger.info("close the app ...")
        self.driver.close_app()

    def quit(self):
        """quit the driver"""
        logger.info("quit the driver ...")
        self.driver.quit()

    def set_ime(self):
        """Set the IME UnicodeIME"""
        logger.info("Set the current IME Appium UnicodeIME")
        try:
            self.driver.activate_ime_engine("io.appium.android.ime/.UnicodeIME")
        except Exception as e:
            logger.info("The Appium UnicodeIME is not installed: %s" % e)

    def assert_in(self, text):
        """verify the current page exist the text, or it will be fail"""
        self.assert_true(self.is_exist_current(text))
        logger.info("Current page not exist %s, fail" % text)

    def assert_not_in(self, text):
        """verify the current page not exist the text, or it will be fail"""
        self.assert_false(self.is_exist_current(text))
        logger.info("Current page exist %s, fail" % text)

    def assert_equal(self, value1, value2):
        """assert equal, or it will be fail"""
        try:
            assert value1 == value2, "%s != %s" % (repr(value1), repr(value2))
        except Exception as msg:
            file = self.driver.get_screenshot_as_file(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach.file('screen shot', content, type=allure.attachment_type.PNG)
            logger.error(msg)

    def assert_not_equal(self, value1, value2):
        """assert not equal, or it will be fail"""
        try:
            assert value1 != value2, "%s != %s" % (repr(value1), repr(value2))
        except Exception as msg:
            file = self.driver.get_screenshot_as_file(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach.file('screen shot', content, type=allure.attachment_type.PNG)
            logger.error(msg)

    def assert_true(self, value):
        """assert true, or it will be fai"""
        try:
            assert value is True, "%s is not true" % str(value)
        except Exception as msg:
            file = self.driver.get_screenshot_as_file(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach.file('screen shot', content, type=allure.attachment_type.PNG)
            logger.error(msg)

    def assert_false(self, value):
        """assert false, or it will be fai"""
        try:
            assert value is False, "%s is not false" % str(value)
        except Exception as msg:
            file = self.driver.get_screenshot_as_file(str(inspect.stack()[1][3]))
            content = open(file, 'rb').read()
            allure.attach.file('screen shot', content, type=allure.attachment_type.PNG)
            logger.error(msg)

    def is_toast_show(self, message, wait=10):
        """check the toast show and use to assert"""
        locator = {'name': '[Toast] %s' % message, 'timeOutInSeconds': wait, 'type': 'xpath',
                   'value': '//*[contains(@text,\'%s\')]' % message}
        try:
            element = self.find_element(*locator)
            return element is not None
        except NoSuchElementException:
            logger.info("[Toast] can't be found: %s" % locator)
            return False

    def toast_assert(self, text):
        """这儿对于一闪而过的，就经常在第二次去找元素，想拿来某属性做断言，提示 找不到元素"""
        assert_result = True
        try:
            WebDriverWait(self.driver, 10, 0.05).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@text, "%s")]' % text[1:3])))
            print('可以找到这个toast')
        except Exception as e:
            print('找不到这个toast: %s' % e)
            assert_result = False

        if assert_result is True:
            TestCase.assertEqual(
                self.driver.find_element_by_xpath('//*[contains(@text, "%s")]' % text[1:3]).get_attribute('text'),
                text, '但是 text断言失败了')
            print('text属性值 断言成功')
        else:
            print("断言失败")

    @staticmethod
    def get_current_time():
        """获取当前时间"""
        temp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        return temp

    def image_to_string(self, locator):
        # 截取当前网页，该网页有我们需要的验证码
        self.driver.save_screenshot(self.path + "/screenshots/" + "pages.png")
        img_element = self.find_element(*locator)
        # 获取验证码x,y轴坐标
        location = img_element.location
        # 获取验证码的长宽
        size = img_element.size
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  # 写成我们需要截取的位置坐标
                  int(location['y'] + size['height']))
        i = Image.open(self.path + "/screenshots/" + "pages.png")
        # 使用Image的crop函数，从截图中再次截取我们需要的区域
        result = i.crop(rangle)
        result.save(self.path + "/screenshots/" + "result.png")
        rgb_im = result.convert('RGB')
        rgb_im.save(self.path + "/screenshots/" + "result.jpg")
        img = Image.open(self.path + "/screenshots/" + "result.jpg")
        img.convert("L")
        verify_code = pytesseract.image_to_string(img).strip()
        logger.info("verify code is: " + verify_code)
        return verify_code

    def get_screenshots_by_slide_up(self, folder_name, img_name, scroll_times=1):
        i = 0
        while i < scroll_times:
            self.get_screenshot(folder_name, img_name + "_" + str(i))
            self.swipe_up()
            self.sleep(2)
            i += 1

    def go_to_top(self, scroll_times=5):
        logger.info("go to top ...")
        for i in range(scroll_times):
            self.swipe_down()
            self.sleep(1)

    def video_screenshots(self, folder_name, img_name):
        self.get_screenshot(folder_name, img_name + "_1")
        self.sleep(8)
        self.get_screenshot(folder_name, img_name + "_2")
        self.sleep(1)

    def get_screenshot_by_element(self, element, folder_name, image_name, image_form="png"):
        # get the whole screenshot
        ele_image_path = folder_name + "/" + image_name + "." + image_form
        whole_image = self.get_screenshot(folder_name, "whole")
        # get the element bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        # cut the image
        image = Image.open(whole_image)
        new_image = image.crop(box)
        new_image.save(ele_image_path)
        os.remove(whole_image)
        logger.info("The element had been saved in %s" % ele_image_path)
        return ele_image_path

    def get_screenshot_by_custom_size(self, file_path, start_x, start_y, end_x, end_y):
        # user defined the image area
        self.driver.get_screenshot_as_file(file_path)
        box = (start_x, start_y, end_x, end_y)
        image = Image.open(file_path)
        new_image = image.crop(box)
        new_image.save(file_path)
        return file_path

    def write_to_file(self, old_file, new_path, image_name, image_form="png"):
        # copy the file
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
        else:
            logger.info("%s is exist" % new_path)
        shutil.copyfile(old_file, new_path + "/" + image_name + "." + image_form)

    def load_image(self, image_path):
        # load the image
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            logger.info("%s is not exist" % image_path)
            raise Exception

    def same_as(self, temp_file, actual_image, percent=0):
        # compare the image，if percent set 0，mean the two images' similarity is 100% and will return True
        # the percent set bigger means the difference more
        image1 = Image.open(temp_file)
        image2 = self.load_image(actual_image)
        histogram1 = image1.histogram()
        histogram2 = image2.histogram()
        differ = math.sqrt(
            reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            return True
        else:
            return False

    def switch_context(self, context="WEBVIEW_xxxx"):
        context = context.upper()
        contexts = self.driver.contexts
        for con in contexts:
            if context in con and context.find('WEBVIEW') != -1:
                logger.info('switch webview')
                self.driver.switch_context(con)
                res = self.driver.current_context
                return True if context in res else False
            elif context in con and context.find('NATIVE') != -1:
                logger.info('switch native')
                self.driver.switch_context(con)
                os.system('pkill -9 chromedriver')
                res = self.driver.current_context
                logger.info(res)
                return True if context in res else False
        return False

    def switch_content_default(self):
        time.sleep(3)
        self.driver.switch_context('NATIVE_APP')
        os.system('pkill -9 chromedriver')
        for con in self.driver.contexts:
            if con.find('WEBVIEW') != -1:
                self.driver.switch_context(con)
                return True
        return False

    def always_allow(self, number=5):
        """install app need to confirm the allow button"""
        for i in range(number):
            loc = ("xpath", "//*[@text='始终允许']")
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except:
                pass
