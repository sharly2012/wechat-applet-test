import time
import yaml
import os
import subprocess
from appium import webdriver
from tomorrow import threads

cur_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.split(cur_path)[0]
cur_time = time.strftime("%Y_%m_%d_%H", time.localtime())


def check_port(port):
    """检测端口是否被占用"""
    a = os.popen('netstat -ano | findstr "%s" ' % port)
    time.sleep(3)
    t1 = a.read()
    if "LISTENING" in t1:
        print("appium服务已经启动或端口已被占用：%s" % t1)
        return False
    else:
        print("端口 %s 可以使用 " % port)
        return True


def start_appium(host, port, udid):
    """启动appium 服务"""
    error_message = ""
    appium_server_url = ""
    bootstrap_port = str(port + 1)
    log_path = root_path + "/logs/appium_" + cur_time + ".log"
    try:
        if check_port(port):
            cmd = 'start /b appium -a ' + host + ' -p ' + str(port) + ' --bootstrap-port ' + str(
                bootstrap_port) + " -U " + udid + " --no-reset --session-override"
            print(cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=open(log_path, 'w'), stderr=subprocess.STDOUT)
            p.wait()
            appium_server_url = 'http://' + host + ':' + str(port) + '/wd/hub'
            print(appium_server_url)
    except Exception as msg:
        error_message = str(msg)
    return appium_server_url, error_message


def get_desired_caps(devices_name='192.168.25.103:5555'):
    """从yaml读取desired_caps配置信息"""
    yaml_path = root_path + "/conf/devices.yaml"
    with open(yaml_path, "r", encoding="utf-8") as f:
        a = f.read()
        f.close()

    devices_list = yaml.load(a, Loader=yaml.FullLoader)
    for device in devices_list:
        if devices_name == device.get("device_name"):
            appium_host = device.get("host")
            appium_port = device.get("port")
            desired_caps = device.get("desired_caps")
            udid = device.get("desired_caps")["udid"]
            return appium_host, appium_port, desired_caps, udid


@threads(2)
def run_app(devices_name):
    desired_caps = get_desired_caps(devices_name)
    print(desired_caps)
    start_appium(desired_caps[0], desired_caps[1], desired_caps[3])
    driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % desired_caps[1], desired_caps[2])
    time.sleep(10)
    driver.find_element_by_xpath("//*[@text='发现']").click()
    time.sleep(5)
    driver.find_element_by_xpath("//*[@text='朋友圈']").click()
    time.sleep(5)
    driver.close_app()


if __name__ == "__main__":
    devices = ["Samsung_GalaxyS9", "google_Pixel2"]
    for i in devices:
        run_app(devices_name=i)
