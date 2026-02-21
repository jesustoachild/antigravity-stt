import base64
import logging
import struct
from collections.abc import AsyncIterable

from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
    SpeechToTextEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_API_KEY,
    CONF_URL,
    CONF_MODEL,
    CONF_LANGUAGE,
    DEFAULT_LANGUAGE,
    SUPPORTED_STT_LANGUAGES,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Antigravity STT provider."""
    async_add_entities([AntigravitySTTEntity(hass, config_entry)])

class AntigravitySTTEntity(SpeechToTextEntity):
    """The Antigravity STT entity v0.1 (Language + i18n)."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the provider."""
        self.hass = hass
        self.entry = entry
        model = entry.options.get(CONF_MODEL) or entry.data.get(CONF_MODEL) or "gemini-3-flash"
        self._attr_name = f"Antigravity STT ({model})"
        self._attr_unique_id = f"{entry.entry_id}_stt"

    @property
    def supported_languages(self) -> list[str]:
        return SUPPORTED_STT_LANGUAGES

    @property
    def supported_formats(self) -> list[AudioFormats]:
        return [AudioFormats.WAV]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        return [AudioCodecs.PCM]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        return [AudioSampleRates.SAMPLERATE_16000, AudioSampleRates.SAMPLERATE_44100, AudioSampleRates.SAMPLERATE_48000]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        return [AudioChannels.CHANNEL_MONO]

    def _add_wav_header(self, pcm_data: bytes, sample_rate: int) -> bytes:
        """Add standard WAV header manually."""
        if not sample_rate or sample_rate < 8000:
            sample_rate = 16000
        
        bits_per_sample = 16
        channels = 1
        byte_rate = sample_rate * channels * bits_per_sample // 8
        block_align = channels * bits_per_sample // 8
        data_size = len(pcm_data)
        chunk_size = 36 + data_size
        
        header = struct.pack(
            '<4sI4s4sIHHIIHH4sI',
            b'RIFF', chunk_size, b'WAVE', b'fmt ',
            16, 1, channels, sample_rate, byte_rate, block_align, bits_per_sample,
            b'data', data_size
        )
        return header + pcm_data

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> SpeechResult:
        """Process audio stream with enhanced structure checking."""
        _LOGGER.debug("Antigravity STT v0.1 processing...")
        raw_audio = b""
        try:
            async for chunk in stream:
                raw_audio += chunk
        except Exception as err:
            _LOGGER.error("Error reading audio stream: %s", err)
            return SpeechResult(None, SpeechResultState.ERROR)

        if not raw_audio:
            _LOGGER.warning("Received empty audio stream")
            return SpeechResult(None, SpeechResultState.ERROR)

        wav_audio = self._add_wav_header(raw_audio, int(metadata.sample_rate))
        base64_audio = base64.b64encode(wav_audio).decode("utf-8")
        
        url = self.entry.data.get(CONF_URL)
        api_key = self.entry.data.get(CONF_API_KEY)
        if not url or not api_key:
            _LOGGER.error("Missing URL or API Key in config")
            return SpeechResult(None, SpeechResultState.ERROR)
        model = self.entry.options.get(CONF_MODEL) or self.entry.data.get(CONF_MODEL) or "gemini-3-flash"
        lang_cfg = self.entry.options.get(CONF_LANGUAGE) or self.entry.data.get(CONF_LANGUAGE) or DEFAULT_LANGUAGE

        # auto = 使用 HA 语言；指定则用配置值
        if lang_cfg == "auto":
            raw = getattr(metadata, "language", None) or self.hass.config.language or "en"
            raw = raw.replace("_", "-")
            if raw.startswith("zh-Hant") or "TW" in raw.upper():
                lang = "zh-TW"
            elif raw.startswith("zh"):
                lang = "zh-CN"
            elif raw.startswith("ja"):
                lang = "ja"
            elif raw.startswith("ko"):
                lang = "ko"
            elif raw.startswith("en"):
                lang = "en-US" if "-" in raw or len(raw) > 2 else "en"
            else:
                lang = raw.split("-")[0] if "-" in raw else raw
        else:
            lang = lang_cfg

        prompt = f"Transcribe the audio to {lang}. ONLY output the transcription text, no punctuation."

        is_openai_url = "chat/completions" in url
        if not is_openai_url:
            payload = {
                "contents": [{"parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "audio/wav", "data": base64_audio}}
                ]}],
                "generationConfig": {"temperature": 0.0}
            }
        else:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": f"You are a professional STT tool. Transcribe to {lang}. ONLY output transcript."},
                    {"role": "user", "content": [{"type": "text", "text": prompt},
                                                {"type": "image_url", "image_url": {"url": f"data:audio/wav;base64,{base64_audio}"}}]}
                ],
                "temperature": 0.0
            }

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        session = async_get_clientsession(self.hass)
        
        try:
            # 增加超时时间到 60s
            async with session.post(url, json=payload, headers=headers, timeout=60) as response:
                if response.status != 200:
                    _LOGGER.error("Antigravity STT HTTP %s: %s", response.status, await response.text())
                    return SpeechResult(None, SpeechResultState.ERROR)
                
                result_json = await response.json()
                
                # 增强型结构解析
                text = ""
                try:
                    if "candidates" in result_json:
                        text = result_json["candidates"][0]["content"]["parts"][0]["text"]
                    elif "choices" in result_json:
                        text = result_json["choices"][0]["message"]["content"]
                    else:
                        _LOGGER.error("Unknown API response structure: %s", result_json)
                        return SpeechResult(None, SpeechResultState.ERROR)
                except (IndexError, KeyError) as e:
                    _LOGGER.error("Failed to parse API result: %s. Response: %s", e, result_json)
                    return SpeechResult(None, SpeechResultState.ERROR)

                # 结果清理
                text = (text or "").replace("。", "").replace(".", "").replace("\"", "").replace("'", "").strip()
                _LOGGER.info("STT v0.1 Result: %s", text)
                return SpeechResult(text, SpeechResultState.SUCCESS)

        except Exception as err:
            _LOGGER.error("Antigravity STT Exception: %s", err)
            return SpeechResult(None, SpeechResultState.ERROR)
