# 验证状态

此文件区分 Windows 上能验证的内容和必须等待 GitHub / iPhone 的内容。实际构建结果以对应 Actions 运行及 `validation.json` 为准。

| 项目 | 当前状态 |
|---|---|
| Python IPA 校验器测试 | 已在 Windows 运行，7 项通过；此前在校验器未实现时观察到失败 |
| Xcode 工程格式 | 使用 OpenStep 解析器解析成功，36 个对象的引用及 Info.plist 路径检查通过 |
| Info.plist / scheme / CI 配置 | 两个 plist、共享 scheme XML、CI YAML 与 LF 行尾检查均通过 |
| Bash 脚本语法 | Git Bash `bash -n scripts/build.sh` 通过 |
| 代码审查 | 完成一次只读审查，未发现明确的编译、扩展嵌入或键盘操作缺陷；不替代编译和实测 |
| Swift / UIKit 编译 | GitHub macOS 构建成功；Xcode 16.4 / iPhoneOS 18.5 SDK，最低部署版本 iOS 16.0 |
| 真实 IPA 结构及二进制 | 已下载真实 IPA，在 Windows 再次校验主 App、键盘扩展与 arm64 iOS device 二进制，通过 |
| 下载完整性 | 本地 SHA-256 与云端校验和一致 |
| 签名、添加键盘、微信、刷新 | 待用户真机验收 |

GitHub CLI 已完成工作流权限授权；公开仓库 [keyboard-install-probe](https://github.com/Quinng988419/keyboard-install-probe) 的 16 个源码文件与云端打包配置均已上传。Windows Git 上传遇到连接超时，改用 API 完成上传。

成功构建：[Actions 39524699060](https://github.com/Quinng988419/keyboard-install-probe/actions/runs/39524699060)，源码提交 `bda4260b6ab265338530358101570d8b9b24536c`，日期 2026-10-21。构建产物 `KeyboardProbe-unsigned.ipa` 为 21,863 字节，尚未签名。

SHA-256：`b0e6b8899cd9f21e0a7f781e3baf833e0e75a16f76d6f15e8ead11e7093f047c`。

主 App ID：`com.codexpersonal.KeyboardProbe`；键盘 ID：`com.codexpersonal.KeyboardProbe.Keyboard`。

当前阻碍真机验收的是数据线接口与电脑不匹配：用户确认电脑只有 USB-A 接口，需要支持数据传输的 USB-A 转 Lightning 数据线，尚未完成手机与电脑连接。因此不能声称 AltStore 安装、微信兼容性或签名刷新已通过。

本版本没有网络代码、账户、AI、剪贴板访问或 App Group。构建不需要任何 Apple 凭证或 API Key。
