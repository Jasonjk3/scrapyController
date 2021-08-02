'''
@author: jasonfor
@contact: jasonforjob@qq.com
@file: deploy.py
@time: 2021/7/28 0028 22:48
@desc:
'''
import zipfile
import subprocess
from application.base import log
import os


class DeployException(Exception):
    '''当输出有误时，抛出此异常'''
    #自定义异常类型的初始化
    def __init__(self, value=None):
        self.value = value
    # 返回异常类对象的说明信息
    def __str__(self):
        return ("commond or deploy error - >{} ".format(repr(self.value)))



def unzip(zip_src, dst_dir):
    """
    解压zip文件
    :param zip_src: zip文件的全路径
    :param dst_dir: 要解压到的目的文件夹
    :return:
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        return "请上传zip类型压缩文件"

def to_egg(file_path,base_name,scrapyd_url,version):
    file_path = file_path + f'\\{base_name}'
    egg_name = base_name+'.egg'
    commond = f'scrapyd-deploy -p {base_name} -v {version} --build-egg={egg_name}'
    try:
        res = subprocess.check_call(commond, shell=True, cwd=file_path)
        if res!=0:
            raise DeployException()
    except Exception as e:
        log.error(f'deploy error! -> {e}')
    egg_file_path =file_path + '\\'+ egg_name
    if os.path.exists(egg_file_path):
        return egg_file_path
    else:
        raise DeployException()
