#!/usr/bin/env python3

import os
import sys
import configparser
import requests
import json

# 1. 读取.izmj/iup.ini文件。
#   1.1 读取iup的更新服务器地址。如果没提供，默认https://izmj.net/release/iup_upgrade.json
#   1.2 读取需要被服务的程序的更新地址。
# 2. 如果iup.ini文件不存在，则创建该文件。
#   2.1 保存默认的iup服务器地址https://izmj.net/release/iup_upgrade.json。
# 3. 如果没有读取到被服务的程序的更新地址。要求用户输入一个。
# 4. 通过--version参数，读取被服务的程序的版本号。

# 默认配置文件位置，可以通过--conf=xxxxx外部设定
IUP_CONF_PATH_DEFAULT = "./.izmj/iup.ini"

# 默认更新地址，可以通过修改conf获得
IUP_UPDATE_URL_DEFAULT = "https://izmj.net/release/iup_upgrade.json"

# 当前程序版本号
IUP_VERSION_MAJOR = "0"
IUP_VERSION_MINOR = "5"
IUP_VERSION_BUILD = "0"

iup_conf_path = IUP_CONF_PATH_DEFAULT

# 遍历入参
for arg in sys.argv:
    if arg.startswith('--conf='):
        # 读取配置文件
        iup_conf_path = arg[7:]
    elif arg.startswith('--version'):
        # 输出版本号
        print(f'{IUP_VERSION_MAJOR}.{IUP_VERSION_MINOR}.{IUP_VERSION_BUILD}')
        sys.exit(0)


iup_update_url = ''
if os.path.exists(iup_conf_path):
    # 读取ini文件
    config = configparser.ConfigParser()
    config.read(iup_conf_path)

    # 读取配置
    iup_update_url = config.get('iup', 'update_url')

else:
    # 创建配置文件
    if not os.path.exists(os.path.dirname(iup_conf_path)):
        os.makedirs(os.path.dirname(iup_conf_path))
    
    config = configparser.ConfigParser()
    config.add_section('iup')
    config.set('iup', 'update_url', IUP_UPDATE_URL_DEFAULT)
    config.write(open(iup_conf_path, 'w'))

# 如果读取配置失败，使用默认的更新路径
if '' == iup_update_url:
    print(f'配置文件[{iup_conf_path}]中未读取到iup更新服务器地址，使用默认路径：' + IUP_UPDATE_URL_DEFAULT)
    iup_update_url = IUP_UPDATE_URL_DEFAULT
else:
    print(f'配置文件[{iup_conf_path}]中读取到iup更新服务器地址：' + iup_update_url)

# 从iup_conf_path上读取最新的版本号，超时时间为5秒
try:
    r = requests.get(iup_update_url, timeout=15)
    if 200 != r.status_code:
        print(f'无法从{iup_update_url}获取最新版本号！请邮件联系作者contact@izmj.net')
        sys.exit(1)
except requests.exceptions.Timeout:
    print('网络超时，请稍后重试。')
    sys.exit(1)

# 解析json
iup_update_info = json.loads(r.text)
iup_update_url_version = iup_update_info['version']
iup_download_url = iup_update_info['download_url']
iup_update_url = iup_update_info['update_url']
iup_changelog = iup_update_info['changelog']

# 解析iup_update_url_version，拆分MAIN.SUB.BUILD
iup_update_url_version_split = iup_update_url_version.split('.')
iup_update_url_version_main = iup_update_url_version_split[0]
iup_update_url_version_sub = iup_update_url_version_split[1]
iup_update_url_version_build = iup_update_url_version_split[2]

# 如果版本号比当前版本号大，则提示更新
if (int(iup_update_url_version_main) <= int(IUP_VERSION_MAJOR)) and (int(iup_update_url_version_sub) <= int(IUP_VERSION_MINOR)) and (int(iup_update_url_version_build) <= int(IUP_VERSION_BUILD)):
    print('当前版本已经是最新版本，无需更新。')
    exit(0)
else:
    print('----------------------------------')
    print(f'发现新版本{iup_update_url_version}，请更新！')
    print(f'更新地址：{iup_download_url}')
    print(f'更新日志：{iup_changelog}')
    print('----------------------------------')
