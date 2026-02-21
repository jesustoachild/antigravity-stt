"""Constants for the Antigravity STT integration."""

DOMAIN = "antigravity_stt"

CONF_API_KEY = "api_key"
CONF_URL = "url"
CONF_MODEL = "model"
CONF_LANGUAGE = "language"

DEFAULT_MODEL = "gemini-3-flash"
DEFAULT_URL = "http://<Antigravity_Tools_IP>:<Port>/v1/chat/completions"
DEFAULT_LANGUAGE = "auto"

# 1. UI 下拉菜单显示的常用语言
SUPPORTED_LANGUAGES = [
    "auto", "zh-CN", "zh-TW", "en-US", "en", "ja", "ko", "de", "fr", "es", "it", "pt", "ru",
]

# 2. 插件上报给 HA 的完整支持列表 (Gemini 3 Flash 核心能力)
# 包含 100+ 种 ISO 语言代码，确保 HA Assist 在任何语言下都能调用此插件
SUPPORTED_STT_LANGUAGES = [
    "af", "am", "ar", "az", "be", "bg", "bn", "bs", "ca", "ceb", "co", "cs", "cy", "da", "de", 
    "el", "en", "en-US", "en-GB", "eo", "es", "et", "eu", "fa", "fi", "fr", "fy", "ga", "gd", 
    "gl", "gu", "ha", "haw", "hi", "hmn", "hr", "ht", "hu", "hy", "id", "ig", "is", "it", 
    "iw", "ja", "jw", "ka", "kk", "km", "kn", "ko", "ku", "ky", "la", "lb", "lo", "lt", 
    "lv", "mg", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my", "ne", "nl", "no", "ny", 
    "or", "pa", "pl", "ps", "pt", "ro", "ru", "sd", "si", "sk", "sl", "sm", "sn", "so", 
    "sq", "sr", "st", "su", "sv", "sw", "ta", "te", "tg", "th", "tl", "tr", "ug", "uk", 
    "ur", "uz", "vi", "xh", "yi", "yo", "zh", "zh-CN", "zh-TW", "zu", "auto"
]
