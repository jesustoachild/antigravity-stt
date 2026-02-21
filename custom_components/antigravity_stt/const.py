"""Constants for the Antigravity STT integration."""

DOMAIN = "antigravity_stt"

CONF_API_KEY = "api_key"
CONF_URL = "url"
CONF_MODEL = "model"
CONF_LANGUAGE = "language"

DEFAULT_MODEL = "gemini-3-flash"
DEFAULT_URL = "http://<Antigravity_Tools_IP>:<Port>/v1/chat/completions"
DEFAULT_LANGUAGE = "auto"

# 这是 UI 下拉菜单显示的语言列表
SUPPORTED_LANGUAGES = [
    "auto",
    "zh-CN",
    "zh-TW",
    "en-US",
    "en",
    "ja",
    "ko",
    "de",
    "fr",
    "es",
    "it",
    "pt",
    "ru",
]

# 供 stt.py 使用的别名，确保兼容性
SUPPORTED_STT_LANGUAGES = SUPPORTED_LANGUAGES
