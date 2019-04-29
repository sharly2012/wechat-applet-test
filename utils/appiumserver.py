import os
import time
import subprocess


class AppiumServer(object):

    @staticmethod
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

    def start_appium(self, host, port, udid, log_path):
        """启动appium 服务"""
        error_message = ""
        appium_server_url = ""
        bootstrap_port = str(port + 1)

        try:
            if self.check_port(port):
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

    @staticmethod
    def stop_appium(post_num=4723):
        """关闭appium服务"""
        p = os.popen('netstat  -aon | findstr %s' % post_num)
        p0 = p.read().strip()
        print(p0)
        if p0 != '' and 'LISTENING' in p0:
            # 获取进程号
            p1 = int(p0.split('LISTENING')[1])
            print(p1)
            # 结束进程
            cmd = "start /b taskkill -f -pid %s" % p1
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print('appium server已结束')
        else:
            print("没有找到端口：%s" % post_num)


if __name__ == '__main__':
    s = AppiumServer()
    s.start_appium('127.0.0.1', 4723, "CLB0219116000104", "D:/111.log")
    time.sleep(10)
    s.stop_appium(4723)
