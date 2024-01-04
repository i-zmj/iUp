# 升级工具 iUp

简单的版本检查脚本。  
Simple version check script.

查询指定服务器路径，获得版本号，更新地址，更新内容等。  
Request UPDATE_URL, VERSION, DOWNLOAD_URL, CHANGE_LOG from server.

## 结构 Structure

## iup_support.py

- 用于支持`--iup-version`，`--iup-update`命令，提供版本信息，更新地址支持。

## iup_upgrade.py

用于升级脚本。

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

## 发布流程 Release Workflow

1. 修改代码，更新`--iup-version`命令返回的版本信息。  
2. 应用打包zip。
3. 更新https://izmj.net/release/iup_upgrade.json内容。
----
1. Modify the code and update the version information returned by the `--iup-version` command.  
2. Make zip package.
3. Update the content of the https://izmj.net/release/iup_upgrade.json.