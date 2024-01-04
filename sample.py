#!/usr/bin/env python3

IUP_CURRENT_VERSION = '0.5.1'
IUP_UPDATE_URL = 'https://gitee.com/izmj/iup/raw/master/lastest.json'

import iup

# 支持--iup-version，--iup-update-url，--iup-upgrade参数
iup.init(IUP_CURRENT_VERSION, IUP_UPDATE_URL)

# 手动触发检查更新。
iup.check_upgrade(IUP_CURRENT_VERSION, IUP_UPDATE_URL)