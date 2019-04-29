import os
import shutil
from utils.logger import Logger
from utils.baseutil import BaseUtil

logger = Logger("basefile").get_log()


def files_and_dirs_list(dir_path):
    """ls the files in the folder"""
    for root, dirs, files in os.walk(dir_path):
        logger.info("The root is: %s" % root)
        logger.info("The dirs are: %s" % dirs)
        logger.info("The files are: %s" % files)


def all_files(dir_path):
    """输出文件夹下所有文件名（不包括文件夹）"""
    for file in os.listdir(dir_path):
        print(file)


def delete_folder(folder_path):
    """delete the folder and the files in the folder"""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        logger.info("The Folder %s had been deleted" % folder_path)
    else:
        logger.info("Folder %s is not exist" % folder_path)


def make_folder(folder_path):
    """create folder"""
    if os.path.exists(folder_path):
        logger.info("Folder %s is exist" % folder_path)
    else:
        os.mkdir(folder_path)
        logger.info("Folder %s is created" % folder_path)


def copy_folder(olddir_path, newdir_path):
    """copy folder，olddir and newdir must be folder type"""
    delete_folder(newdir_path)
    if os.path.exists(newdir_path):
        shutil.rmtree(newdir_path)
    shutil.copytree(olddir_path, newdir_path)


if __name__ == '__main__':
    screenshots_folder = BaseUtil().root_path + "/screenshots/恭和家园"
    make_folder(screenshots_folder)
    current_time = BaseUtil().get_current_time()
    result_images = screenshots_folder + "/" + current_time
    make_folder(result_images)
