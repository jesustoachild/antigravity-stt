"""Constants for the Antigravity STT integration."""
DOMAIN = "antigravity_stt"
CONF_API_KEY = "api_key"
CONF_URL = "url"
CONF_MODEL = "model"
CONF_LANGUAGE = "language"

DEFAULT_MODEL = "gemini-3-flash"
DEFAULT_URL = "http://192.168.31.18:28045/v1/chat/completions"
DEFAULT_LANGUAGE = "auto"

# auto = 使用 HA 语言；其它为指定输出语言（Gemini 支持多种语言，此处列出常用）
SUPPORTED_LANGUAGES = [
    "auto",
    "zh",
    "zh-CN",
    "zh-TW",
    "en",
    "en-US",
    "en-GB",
    "ja",
    "ja-JP",
    "ko",
    "ko-KR",
    "fr",
    "fr-FR",
    "de",
    "de-DE",
    "es",
    "es-ES",
    "it",
    "it-IT",
    "pt",
    "pt-BR",
    "ru",
    "ru-RU",
    "ar",
    "hi",
    "hi-IN",
    "th",
    "th-TH",
    "vi",
    "vi-VN",
    "id",
    "id-ID",
]

# STT 实体支持的语言（不含 auto）
SUPPORTED_STT_LANGUAGES = [l for l in SUPPORTED_LANGUAGES if l != "auto"]
