# Antigravity STT 插件评价

> 基于 V12，最后更新：2025-02

## 结构概览

Home Assistant 自定义 STT 集成，对接 Gemini Native 或 OpenAI 兼容 API。目录结构：

```
antigravity_stt/
├── __init__.py        # 入口与加载逻辑
├── config_flow.py     # 配置流程
├── const.py           # 常量
├── manifest.json      # 元数据与依赖
├── stt.py             # STT 实现
├── strings.json       # 英文默认文案
├── translations/      # 多语言
│   ├── zh-Hans.json   # 简体中文
│   ├── zh-Hant.json   # 繁体中文
│   ├── ja.json        # 日语
│   ├── ko.json        # 韩语
│   └── de.json        # 德语
└── EVALUATION.md      # 本评价文档
```

---

## 优点

| 项目 | 说明 |
|------|------|
| 双协议适配 | 根据 URL 自动切换 Gemini Native / OpenAI chat/completions |
| aiohttp 复用 | 使用 `async_get_clientsession`，符合 HA 推荐方式 |
| 音频处理 | 手动构造 WAV 头，支持 16k/44.1k/48k 采样率 |
| 配置流 | URL、API Key、Model、Language 可在 UI 中配置 |
| Options Flow | 集成选项可修改 Model、Language |
| 语言提示 | 支持 auto（HA 语言）/ 指定语言，提示词含 "Transcribe to {lang}" |
| 多语言界面 | strings.json + translations（zh-Hans/zh-Hant/ja/ko/de），缺省英文 |
| 错误处理 | HTTP、解析异常、通用异常均有处理 |
| 日志 | debug / info / warning / error 分层清晰 |

---

## 已修复项

| 项目 | 状态 |
|------|------|
| manifest 依赖 | ✅ 无多余依赖 |
| API 解析异常 | ✅ `try/except (IndexError, KeyError)` 结构检查 |
| 超时 | ✅ 60 秒 |
| 空音频 | ✅ `_LOGGER.warning` 记录 |
| 未使用导入 | ✅ 已清理 |
| text 为 None | ✅ `(text or "")` 防护 |

---

## 可选改进

| 项目 | 说明 |
|------|------|
| OpenAI audio 格式 | `image_url` 传递音频为后端扩展，若换用标准 API 需调整 |
| 配置校验 | 可增加 URL 格式、API Key 非空校验 |

---

## 功能与兼容性

| 项目 | 状态 |
|------|------|
| 流式处理 | 否，先收集完整音频再发送 |
| 支持语言 | zh, zh-CN, zh-TW, en, en-US, ja, ko, fr, de, es, … |
| 音频格式 | WAV (PCM 16-bit mono) |
| 采样率 | 16000, 44100, 48000 Hz |
| 配置流 | ✅ |
| 卸载逻辑 | ✅ |

---

## 结论

V12 实现稳健，支持语言配置与多语言界面，适合作为日常使用的 HA 自定义 STT 集成。
