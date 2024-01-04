#!/usr/bin/env python3

IUP_VERSION = '0.4.1'
IUP_UPDATE_URL = 'https://gitee.com/izmj/iup/raw/master/VERSION'

import iup_support

# 支持--iup-version和--iup-update-url参数
iup_support.init(IUP_VERSION, IUP_UPDATE_URL)
iup_support.check_upgrade(IUP_VERSION, IUP_UPDATE_URL)