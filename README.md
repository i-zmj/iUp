# 升级工具 iUp

简单的版本检查脚本。  
Simple version check script.

查询指定服务器路径，获得版本号，更新地址，更新内容等。  
Request UPDATE_URL, VERSION, DOWNLOAD_URL, CHANGE_LOG from server.

## 结构 Structure

## iup.py

支持`--iup-version`，`--iup-update-url`，`--iup-upgrade`命令

- `--iup-version`：获得iup可读取的版本信息。需要参考【版本号格式】进行定义。
- `--iup-update-url`：获得iup可读取的更新服务器信息。可以参考【lastest.json】进行定义。
- `--iup-upgrade`：执行更新。

## lastest.json

需要放在服务器上的版本信息文件。  
iup的测试sample是利用Gitee的raw路径实现python读取。  
例如sample.py中，

```python
IUP_UPDATE_URL = 'https://gitee.com/izmj/iup/raw/master/lastest.json'
```

## sample.py

使用范例

## 版本号格式 VERSION Format

应用应在接受`--iup-version`参数时，返回版本信息。  
The app should return the version information when accepting the `--iup-version` parameter.  

> 主版本号.次版本号.编译号  
> Major.Minor.Build

- 主版本号：大规模功能变更，可能出现无法兼容前版本的情况。
- 次版本号：普通功能变更，应尽可能兼容前版本。
- 编译号：修正缺陷，无功能变更。
----
- Major version number: Large-scale feature changes, which may not be compatible with previous versions.
- Minor version number: Common feature changes should be compatible with previous versions as much as possible.
- Build number: Fixed bugs, no functional changes.
