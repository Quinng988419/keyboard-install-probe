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

GitHub CLI 已登录 Quinng988419；公开仓库 [keyboard-install-probe](https://github.com/Quinng988419/keyboard-install-probe) 已创建。已通过 API 上传 15 个普通源码文件，并核对其 Git blob 哈希与本地提交一致。Windows Git 上传遇到连接超时，改用 API 完成源码上传。

工作流配置写入被 GitHub 拒绝：当前 CLI 的默认权限不包含 `workflow`。已发起补充授权，待用户在设备登录页完成后上传配置并启动 Actions。因此尚未生成真实 IPA；本地 `.github/workflows/build.yml` 已就绪。

本版本没有网络代码、账户、AI、剪贴板访问或 App Group。构建不需要任何 Apple 凭证或 API Key。
