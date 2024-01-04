#!/usr/bin/env python3

import sys
import requests
import json

def init(version, update_url):

    # 如果没有定义IUP_VERSION，则抛异常
    if '--iup-version' in sys.argv:
        print(version)
        sys.exit(0)
    if '--iup-update-url' in sys.argv:
        print(update_url)
        sys.exit(0)

def check_upgrade(version, update_url):
    # 从iup_conf_path上读取最新的版本号，超时时间为5秒
    try:
        r = requests.get(update_url, timeout=15)
        if 200 != r.status_code:
            print(f'无法从{update_url}获取最新版本号！请邮件联系作者contact@izmj.net')
            sys.exit(1)
    except requests.exceptions.Timeout:
        print('网络超时，请稍后重试。')
        sys.exit(1)

    # 解析json
    iup_update_info = json.loads(r.text)
    iup_remote_version = iup_update_info['version']
    iup_download_url = iup_update_info['download_url']

    try:
        iup_changelog = iup_update_info['changelog']
    except:
        iup_changelog = '无'

    # 解析iup_update_url_version，拆分MAIN.SUB.BUILD
    iup_remote_version_split = iup_remote_version.split('.')
    iup_remote_version_main = iup_remote_version_split[0]
    iup_remote_version_sub = iup_remote_version_split[1]
    iup_remote_version_build = iup_remote_version_split[2]

    iup_current_version_split = version.split('.')
    iup_current_version_main = iup_current_version_split[0]
    iup_current_version_sub = iup_current_version_split[1]
    iup_current_version_build = iup_current_version_split[2]

    # 如果版本号比当前版本号大，则提示更新
    if (int(iup_remote_version_main) <= int(iup_current_version_main)) \
        and (int(iup_remote_version_sub) <= int(iup_current_version_sub)) \
            and (int(iup_remote_version_build) <= int(iup_current_version_build)):
        print(f'当前版本[{version}]已经是最新版本')
        exit(0)
    else:
        print('----------------------------------')
        print(f'- 当前版本：[{version}]')
        print(f'- 发现新版本：[{iup_remote_version}]')
        print(f'- 更新日志：\n----------------------------------\n{iup_changelog}\n----------------------------------')
        print(f'- 更新命令：python iup_upgrade.py --update-url={update_url}')
        print('----------------------------------')