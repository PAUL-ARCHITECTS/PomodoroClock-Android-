# 🍅 番茄时钟 v1.9 (Android 7.0–17)

Android 离线番茄时钟，包含 iOS 风格界面、预设时长、短休息/长休息、通知栏倒计时、快捷设置磁贴和本地统计。

## 编译与下载

点击 **Actions → Build Pomodoro v1.9 APK (Android 7 to 17)**，打开最新的成功运行，下载 **PomodoroClock-v1.9-Android7-17**。该构建产物是调试签名 APK；若与手机上原有 APK 签名不同，不能直接覆盖安装。

## Android 版本

- `minSdk = 24`：Android 7.0
- `compileSdk = 37`：Android 17
- `targetSdk = 37`：Android 17
- AGP 9.4.0 + Gradle 9.6.0 + Java 17
- Java + WebView，无 native `.so` 架构限制

## 代码组织

目前仓库在 `payload/part00.txt` 到 `part04.txt` 中保存压缩的 v1.8 基础项目，由工作流解包，并使用 `scripts/upgrade-v19.py` 应用 v1.9 更新后编译。完整 v1.9 源码压缩包另附在聊天中。

## 兼容修复

- Android 7–9 不调用仅 Android 10+ 支持的 QS 磁贴副标题。
- Android 7 通知使用旧构造方法。
- Android 13+ 请求通知权限。
- Android 7–8 正确使用状态栏 / 导航栏兼容判断。
- 自适应图标解决双层白边，保留旧系统的 full-bleed 启动图标。
- 统一磁贴、应用和通知的本地状态机；切换到下一阶段后需手动启动。
- Android 厂商可能限制磁贴刷新频率；精确提醒可能需要特别授权。

**提示**：跨版本代码已做兼容适配，不代表所有 Android 7–17 设备都已经经过真机测试。
