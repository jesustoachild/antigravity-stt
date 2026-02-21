# Antigravity STT v10 - 技术设计与安装手册

## 1. 项目简介
本项目是一个为 Home Assistant (HA) 设计的高性能语音识别 (STT) 插件，旨在通过 Gemini 3 Flash 实现极速 (<2s) 的语音指令转录。它解决了 HA 2024.11+ 版本中的类名兼容性问题及裸 PCM 流的协议适配问题。

## 2. 技术设计 (Architecture)
### 2.1 音频处理 (The PCM-to-WAV Bridge)
HA Assist 引擎发送的是 **16000Hz / 16-bit / Mono** 的裸采样数据（Raw PCM）。
本插件通过 Python `struct` 模块，在内存中动态构造 44 字节的 RIFF/WAVE 标准头。这确保了发送给 API 的数据被正确识别为音频文件，而非乱码。

### 2.2 双协议智能自适应
V10 版本支持两种 Payload 模式：
- **OpenAI 兼容模式**：通过 `image_url` 伪装 Data URI。适用于大多数三方 API 网关。
- **Gemini Native 模式**：使用 `inline_data` 结构。这是 Google 的原生路径，最稳定，可绕过网关对多模态数据的类型校验。

## 3. 安装方法 (Installation)
1. 将 `antigravity_stt` 文件夹复制到 Home Assistant 配置目录下的 `custom_components/` 文件夹中。
2. 重启 Home Assistant。
3. 在 HA UI 中：`配置` -> `设备与服务` -> `添加集成` -> 搜索 `Antigravity STT`。

## 4. 配置参数
- **URL**: 
  - 如果使用中转网关：填写 `https://your-gateway.com/v1/chat/completions`
  - 如果使用原生 Google 路径：填写 `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
- **API Key**: 您的 API 密钥。
- **Model**: `gemini-3-flash` (推荐)。

## 5. 开发建议
本项目由 ChenLi 提出并由 Antigravity 设计，主要针对中文家居控制指令进行了 Prompt 优化（Temperature=0.0）。
