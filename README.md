# Antigravity STT v0.1

[English](#english) | [简体中文](#简体中文)

---

<a name="english"></a>
## English

### 1. Project Introduction
This is a Speech-to-Text (STT) plugin designed for Home Assistant (HA). It leverages **Antigravity Tools** and the **Gemini 3 Flash API** for transcription. It addresses class name compatibility in HA 2024.11+ and handles protocol adaptation for raw PCM streams.

Tested with [Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager).

### 2. Architecture
#### 2.1 Audio Processing (PCM-to-WAV Bridge)
HA Assist sends raw **16000Hz / 16-bit / Mono** PCM samples. This plugin uses the Python `struct` module to dynamically construct a 44-byte RIFF/WAVE header in memory, ensuring the API correctly identifies the data as an audio file.

#### 2.2 Dual-Protocol Adaptive Logic
Supports two payload modes:
- **OpenAI Compatible**: Uses `image_url` data URIs. Works with most third-party API gateways.
- **Gemini Native**: Uses the `inline_data` structure. This is the direct Google path, bypassing gateway MIME type restrictions.

### 3. Installation
1. Copy the `antigravity_stt` folder to your HA `custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings** -> **Devices & Services** -> **Add Integration** -> Search for **Antigravity STT**.

### 4. Configuration
- **URL**: 
  - For Gateways: `http://<Antigravity_Tools_IP>:<Port>/v1/chat/completions`
- **API Key**: Your API Key. (If the URL points to an Antigravity proxy server, please obtain the key from the Antigravity proxy server settings page.)
- **Model**: `gemini-3-flash` (Recommended).

### 5. License & Credits
- **Copyright**: © 2026 ChenLi
- **Acknowledgments**: Thanks to the [Home Assistant](https://github.com/home-assistant/core) community and relevant open-source projects for their reference and support.

---

<a name="简体中文"></a>
## 简体中文

### 1. 项目简介
本项目是一个为 Home Assistant (HA) 设计的语音识别 (STT) 插件，旨在通过 **Antigravity Tools** 和 **Gemini 3 Flash API** 实现语音指令转录。它解决了 HA 2024.11+ 版本中的类名兼容性问题及裸 PCM 流的协议适配问题。

目前已通过 [Antigravity-Manager](https://github.com/lbjlaq/Antigravity-Manager) 后端集成的完整测试。

### 2. 技术设计
#### 2.1 音频处理 (PCM-to-WAV 桥接)
HA Assist 引擎发送的是 **16000Hz / 16-bit / Mono** 的裸采样数据（Raw PCM）。本插件通过 Python `struct` 模块，在内存中动态构造 44 字节的 RIFF/WAVE 标准头，确保数据被正确识别为音频文件。

#### 2.2 双协议智能自适应
支持两种 Payload 模式：
- **OpenAI 兼容模式**：通过 `image_url` 伪装 Data URI。适用于大多数三方 API 网关。
- **Gemini Native 模式**：使用 `inline_data` 结构。这是 Google 的原生路径，最稳定，可绕过网关对多模态数据的类型校验。

### 3. 安装方法
1. 将 `antigravity_stt` 文件夹复制到 Home Assistant 配置目录下的 `custom_components/` 文件夹中。
2. 重启 Home Assistant。
3. 在 HA UI 中：`配置` -> `设备与服务` -> `添加集成` -> 搜索 `Antigravity STT`。

### 4. 配置参数
- **URL**: 
  - 如果使用中转网关：填写 `http://<Antigravity_Tools_IP>:<Port>/v1/chat/completions`
- **API Key**: 您的 API 密钥（如果 URL 是指向 Antigravity 反代服务器，请在 Antigravity 反代服务器的设置页面获取密钥）。
- **Model**: `gemini-3-flash` (推荐)。

### 5. 版权与致谢
- **版权声明**: © 2026 ChenLi
- **致谢**: 感谢 [Home Assistant](https://github.com/home-assistant/core) 开源社区及相关参考项目提供的技术支持与灵感。
