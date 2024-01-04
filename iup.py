#!/usr/bin/env python3

import sys
import requests
import json
import os
import shutil
import urllib
import zipfile

def upgrade(iup_current_version, iup_update_url):

    iup_download_url = check_upgrade(iup_current_version, iup_update_url)

    # 下载更新
    print(f'正在从{iup_download_url}下载更新...')

    # 删除目录
    if os.path.exists('.iup/'):
        if os.path.isdir('.iup/'):
            shutil.rmtree('.iup/')

    # 创建目录
    os.mkdir('.iup/')

    file_name = iup_download_url.split('/')[-1]

    try:
        urllib.request.urlretrieve(iup_download_url, f'.iup/{file_name}')
    except:
        print(f'无法从{iup_download_url}下载更新！')
        sys.exit(1)

    # 解压更新
    print(f'正在解压...')
    zip_file_path = f'.iup/{file_name}'
    extract_path = '.iup/'

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except:
        print(f'无法解压更新！')
        sys.exit(1)

    # 删除压缩包
    os.remove(zip_file_path)

    # 将.iup/目录下的文件复制到当前目录
    print(f'正在执行更新...')
    source_dir = '.iup/'
    destination_dir = './'

    try:
        shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
    except:
        # 提示复制失败的文件信息
        print(f'更新失败！')
        sys.exit(1)

    print('更新成功')
    sys.exit(0)

def init(iup_current_version, iup_update_url):

    iup_update_url = iup_update_url

    # 如果没有定义VERSION，则抛异常
    if '--iup-version' in sys.argv:
        print(iup_current_version)
        sys.exit(0)
    if '--iup-update-url' in sys.argv:
        print(iup_update_url)
        sys.exit(0)
    if '--iup-upgrade' in sys.argv:
        upgrade(iup_current_version, iup_update_url)

def check_upgrade(iup_current_version, iup_update_url):
    # 从conf_path上读取最新的版本号，超时时间为5秒
    try:
        r = requests.get(iup_update_url, timeout=15)
        if 200 != r.status_code:
            print(f'无法从{iup_update_url}获取最新版本号！请邮件联系作者contact@izmj.net')
            sys.exit(1)
    except requests.exceptions.Timeout:
        print('网络超时，请稍后重试。')
        sys.exit(1)

    # 解析json
    update_info = json.loads(r.text)

    try:
        iup_remote_version = update_info['version']
    except:
        print(f'无法从{iup_update_url}获取version！')
        sys.exit(1)

    try:
        iup_download_url = update_info['download_url']
    except:
        print(f'无法从{iup_update_url}获取download_url！')
        sys.exit(1)

    try:
        changelog = update_info['changelog']
    except:
        changelog = '无'

    # 解析update_url_version，拆分MAIN.SUB.BUILD
    iup_remote_version_split = iup_remote_version.split('.')
    iup_remote_version_main = iup_remote_version_split[0]
    iup_remote_version_sub = iup_remote_version_split[1]
    iup_remote_version_build = iup_remote_version_split[2]

    current_version_split = iup_current_version.split('.')
    current_version_main = current_version_split[0]
    current_version_sub = current_version_split[1]
    current_version_build = current_version_split[2]

    # 如果版本号比当前版本号大，则提示更新
    if (int(iup_remote_version_main) <= int(current_version_main)) \
        and (int(iup_remote_version_sub) <= int(current_version_sub)) \
            and (int(iup_remote_version_build) <= int(current_version_build)):
        print('----------------------------------')
        print(f'- 当前版本[{iup_current_version}]已经是最新版本')
        print('----------------------------------')
        exit(0)
    else:
        print('----------------------------------')
        print(f'- 当前版本：[{iup_current_version}]')
        print(f'- 发现新版本：[{iup_remote_version}]\n')
        print(f'- 更新日志：\n----------------------------------\n{changelog}\n----------------------------------')
        print(f'- 更新命令：python3 {sys.argv[0]} --iup-upgrade')
        print('----------------------------------')
        return iup_download_url