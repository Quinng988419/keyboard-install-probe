# 测试键盘：先验证安装

这是为 iPhone 13 Pro Max / iOS 26.3 准备的原生键盘测试项目。它只插入固定文字、删除一个字符和切换键盘，尚未接入 AI。当前版本无需「允许完全访问」，不读取剪贴板、不联网，也不保存输入内容。

**源码 ZIP 不能安装到 iPhone。需要先在 GitHub 完成构建，再下载生成的 IPA，经 AltStore 签名安装。是否兼容你的微信版本，以真机测试为准。**

## 1. 云端生成 IPA

代码可以在 Windows 编辑；编译由 GitHub Actions 的 macOS 环境完成，不需要在 Windows 安装 Xcode。

公开测试仓库：[Quinng988419/keyboard-install-probe](https://github.com/Quinng988419/keyboard-install-probe)。仓库只包含本项目源码，不包含 Apple 账号、证书、API Key 或聊天记录。源码上传与工作流上传是两个步骤；GitHub CLI 写入 `.github/workflows` 还需要 `workflow` 权限，首次默认登录不包含该权限，需要在设备登录页补充授权。

也可以自行上传：

1. 在 GitHub 创建名为 `keyboard-install-probe` 的空公开仓库。
2. 将本目录内容上传到仓库根目录，包含 `.github/workflows/build.yml`。不能多套一层 `KeyboardProbe` 目录；不要上传 `build`、`dist`、源码 ZIP 或账号信息。
3. 打开仓库的 **Actions → Build keyboard IPA**。推送到 `main` 会自动构建，也可以点击 **Run workflow**。
4. 等运行成功，在页面底部 **Artifacts** 下载 `KeyboardProbe-unsigned` 并解压，找到 `KeyboardProbe-unsigned.ipa`。
5. 如果失败，下载 `KeyboardProbe-build-log`；没有日志时，查看失败步骤，保存错误原文。

构建只使用仓库的只读权限，不需要配置 GitHub Secrets 或 Apple 凭证。公开仓库的标准运行器使用规则见 [GitHub 官方文档](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job)。

## 2. Windows 安装 AltStore Classic

按 [AltStore 官方 Windows 指南](https://faq.altstore.io/altstore-classic/how-to-install-altstore-windows) 准备 Apple 的 iTunes、iCloud 和 AltServer。依赖版本与下载入口以该指南为准；已有 Microsoft Store 版 iCloud 时先看官方故障排查，不要直接卸载现有软件。

- 用数据线连接并解锁 iPhone，在手机上信任这台电脑。
- 按官方指南配置 iTunes 的 Wi-Fi 同步，从 AltServer 托盘菜单选择 **Install AltStore → 你的 iPhone**。
- Apple 账号登录、密码及验证码由你在对应软件中输入，不放进源码或聊天。
- 按手机提示信任开发者；如果系统要求，前往 **设置 → 隐私与安全性 → 开发者模式** 开启并完成重启确认。

这里使用 **AltStore Classic**。先安装并能打开 AltStore，再安装我们的测试包。

## 3. 安装测试包

1. 把 `KeyboardProbe-unsigned.ipa` 传到 iPhone 的「文件」App，例如通过自己使用的文件传输工具。注意传的是 IPA，不是下载外层的 ZIP。
2. 保持 Windows 上 AltServer 运行，并让手机能连接这台电脑。
3. 在 AltStore 的 **My Apps** 页面点 **＋**，选择 IPA。
4. 如果提示是否保留扩展，选择保留所有扩展。`ProbeKeyboard.appex` 就是键盘，不能删除。
5. 等待签名和安装完成。桌面出现「测试键盘」后先打开一次。

免费账号存在侧载 App 数量和 App ID 配额限制；键盘扩展也使用 App ID，见 [AltStore App IDs 说明](https://faq.altstore.io/altstore-classic/app-ids)。遇到配额提示先记录错误，不要删除你已有的应用。

## 4. 添加键盘并验收

前往 **设置 → 通用 → 键盘 → 键盘 → 添加新键盘**，在第三方键盘列表选择「测试键盘」。本版本保持「允许完全访问」关闭即可。[Apple 添加键盘说明](https://support.apple.com/guide/iphone/add-or-change-keyboards-iph73b71eb/ios)

打开测试 App 的输入框，长按系统键盘上的地球键，选择「测试键盘」。按 [真机验收表](docs/ACCEPTANCE.md) 依次测试本 App、备忘录、微信。

期望行为：

- 点一次「插入测试文字」，当前光标处出现 `测试键盘已成功输入。`。
- 再点一次，追加同一句；不会自动发送。
- 点「删除」，删除光标前一个字符；空输入框点删除不会崩溃。
- 「切换键盘」可以回到原来的输入法；长按可显示系统的输入法选择菜单。
- 输入框中已有文字时，插入不会清空原有内容。

密码框会使用系统键盘；部分 App 可以禁用第三方键盘。这些是 [iOS 键盘扩展的系统限制](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/CustomKeyboard.html)。

## 5. 刷新签名

免费签名的应用有七天有效期。请在到期前，让 iPhone 能连接运行 AltServer 的 Windows，在 AltStore 的 **My Apps → Refresh All** 刷新；同时检查 AltStore 自身和测试 App 的剩余天数。[AltStore 有效期说明](https://faq.altstore.io/altstore-classic/your-altstore)

至少实际刷新一次，然后重开微信测试插入和切换。后台刷新可能失败，不能只依赖它。无需仅为刷新签名而重新编译；如果已到期且 AltStore 打不开，按官方指南从 AltServer 重新安装 AltStore，再刷新。

## 问题定位

| 现象 | 先检查什么 |
|---|---|
| Actions 构建失败 | 打开失败步骤和 `KeyboardProbe-build-log`，记录错误原文 |
| IPA 校验失败 | 不安装该产物，检查扩展是否被嵌入、是否误用模拟器构建 |
| AltStore 安装失败 | 保留完整错误；检查开发者模式、账号、配额、电脑连接，区分签名错误和设备不兼容 |
| 主 App 有了，添加列表没有键盘 | 是否保留 `ProbeKeyboard.appex`；先打开主 App，再重新进入键盘设置 |
| 添加了，但微信找不到 | 先在本 App 和备忘录切换测试；核对微信版本，区分系统注册与微信兼容问题 |
| 打开键盘即消失或崩溃 | 保存发生时间及对应系统崩溃日志，检查扩展加载；重装前先保留错误证据 |
| 过几天突然打不开 | 检查签名是否过期、AltServer 是否运行、刷新是否成功 |

需要协作排查时，提供错误原文、出问题的步骤、微信版本与 iOS 版本；不用提供真实聊天内容。

## 本地检查与项目结构

Windows 或 macOS 均可运行：

```console
python -m unittest discover -s tests -v
```

macOS + Xcode 可运行：

```console
bash scripts/build.sh
```

构建产物位于 `dist/KeyboardProbe-unsigned.ipa`，报告为 `dist/validation.json`。打包校验会拒绝缺失键盘扩展、无效入口、缺少可执行文件、错误 Bundle ID、模拟器二进制以及意外开启完全访问的包。校验不是签名或真机兼容性证明。

`App/` 是安装说明与本地测试输入框；`Keyboard/` 是键盘扩展；`KeyboardProbe.xcodeproj` 是原生 Xcode 工程；`.github/workflows/build.yml` 是云端构建配置。最低部署版本设为 iOS 16，但本次验收仅针对你的 iOS 26.3，不宣称已覆盖其他版本。
