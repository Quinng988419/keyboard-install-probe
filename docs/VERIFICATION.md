# 验证状态

此文件区分 Windows 上能验证的内容和必须等待 GitHub / iPhone 的内容。实际构建结果以对应 Actions 运行及 `validation.json` 为准。

| 项目 | 当前状态 |
|---|---|
| Python IPA 校验器测试 | 已在 Windows 运行，7 项通过；此前在校验器未实现时观察到失败 |
| Xcode 工程格式 | 使用 OpenStep 解析器解析成功，36 个对象的引用及 Info.plist 路径检查通过 |
| Info.plist / scheme / CI 配置 | 两个 plist、共享 scheme XML、CI YAML 与 LF 行尾检查均通过 |
| Bash 脚本语法 | Git Bash `bash -n scripts/build.sh` 通过 |
| 代码审查 | 完成一次只读审查，未发现明确的编译、扩展嵌入或键盘操作缺陷；不替代编译和实测 |
| Swift / UIKit 编译 | 待 GitHub macOS 构建；Windows 没有 Xcode，不能本地验证 |
| 真实 IPA 结构及二进制 | 待构建后运行校验器；测试用合成档案不是安装包 |
| 签名、添加键盘、微信、刷新 | 待用户真机验收 |

GitHub CLI 已从官方发行页下载到工作目录。首次设备登录因 CLI 未沿用系统代理而超时；重试已配置进程内代理，目前等待用户完成新的设备登录。尚未创建远程仓库或触发 Actions；首次设备码不应再使用。

本版本没有网络代码、账户、AI、剪贴板访问或 App Group。构建不需要任何 Apple 凭证或 API Key。
