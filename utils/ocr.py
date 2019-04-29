import configparser
import os
from aip import AipOcr


class OCR(object):

    def __init__(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.split(cur_path)[0]
        conf = configparser.ConfigParser()
        conf.read(root_path + "/conf/config.ini")
        app_id = conf.get("OCR", "APP_ID")
        api_key = conf.get("OCR", "API_KEY")
        secret_key = conf.get("OCR", "SECRET_KEY")
        self.client = AipOcr(app_id, api_key, secret_key)

    def get_file_content(self, file_path):
        try:
            with open(file_path, 'rb') as fp:
                return fp.read()
        except Exception as e:
            print(e)

    def get_ocr_words(self, file_path):
        """ 调用通用文字识别, 图片参数为本地图片 """
        words_list = []
        image = self.get_file_content(file_path)
        response = self.client.basicGeneral(image)
        words_length = response.get("words_result_num")
        for i in range(words_length):
            words_list.append(response.get("words_result")[i]["words"])
            print(response.get("words_result")[i]["words"])
        return words_list

    def get_ocr_words_option(self, filePath):
        """ 带参数调用通用文字识别, 图片参数为本地图片 """
        words_list = []
        image = self.get_file_content(filePath)
        options = {"language_type": "CHN_ENG",
                   "detect_direction": "true",
                   "detect_language": "true",
                   "probability": "true"
                   }
        response = self.client.basicGeneral(image, options)
        words_length = response.get("words_result_num")
        for i in range(words_length):
            words_list.append(response.get("words_result")[i]["words"])
            print(response.get("words_result")[i]["words"])
        return words_list


if __name__ == '__main__':
    file_path = "E:/PycharmProjects/wechat_test/screenshots/长安金茂府/2019-04-17_16/" + \
                "2019-04-17_16-56-09_renwufangtan" + ".png"
    ocr = OCR()
    ll = ocr.get_ocr_words(file_path)
    print("***************************")
    # ocr.get_ocr_words_option(file_path)
