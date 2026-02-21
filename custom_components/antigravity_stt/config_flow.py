"""Config flow for Antigravity STT integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_URL,
    CONF_MODEL,
    CONF_LANGUAGE,
    DEFAULT_URL,
    DEFAULT_MODEL,
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
)


class AntigravitySTTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Antigravity STT."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            if not (user_input.get(CONF_URL) or "").strip():
                errors["base"] = "invalid_url"
            elif not (user_input.get(CONF_API_KEY) or "").strip():
                errors["base"] = "invalid_auth"
            else:
                return self.async_create_entry(title="Antigravity STT", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default=DEFAULT_URL): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): str,
                    vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(
                        SUPPORTED_LANGUAGES
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Return options flow."""
        return AntigravitySTTOptionsFlow(config_entry)


class AntigravitySTTOptionsFlow(OptionsFlow):
    """Options flow for Antigravity STT."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_MODEL,
                        default=self.config_entry.options.get(
                            CONF_MODEL,
                            self.config_entry.data.get(CONF_MODEL, DEFAULT_MODEL),
                        ),
                    ): str,
                    vol.Optional(
                        CONF_LANGUAGE,
                        default=self.config_entry.options.get(
                            CONF_LANGUAGE,
                            self.config_entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                        ),
                    ): vol.In(SUPPORTED_LANGUAGES),
                }
            ),
        )
