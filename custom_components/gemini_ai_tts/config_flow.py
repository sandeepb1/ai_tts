"""Config flow for Gemini AI TTS/STT integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_MODEL,
    CONF_VOICE,
    CONF_STYLE,
    CONF_EMOTION,
    CONF_PACE,
    CONF_LANGUAGE,
    CONF_STREAMING,
    CONF_MULTI_SPEAKER,
    CONF_STT_PROJECT_ID,
    CONF_STT_CREDENTIALS_JSON,
    CONF_STT_LANGUAGE,
    CONF_STT_MODEL,
    DEFAULT_MODEL_TTS,
    DEFAULT_VOICE,
    DEFAULT_STYLE,
    DEFAULT_LANGUAGE,
    DEFAULT_STREAMING,
    DEFAULT_STT_LANGUAGE,
    DEFAULT_STT_MODEL,
    MODELS,
    VOICES,
    SPEECH_STYLES,
    EMOTIONS,
    PACE_OPTIONS,
    SUPPORTED_LANGUAGES,
    STT_SUPPORTED_LANGUAGES,
    STT_MODELS,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_NAME, default="Gemini AI TTS"): str,
        vol.Optional(CONF_STT_PROJECT_ID): str,
        vol.Optional(CONF_STT_CREDENTIALS_JSON): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    
    # Test the API key by making a simple request
    try:
        from google import genai
        
        client = genai.Client(api_key=data[CONF_API_KEY])
        # Test with a simple request
        response = client.models.list()
        
        # Check if we can access TTS models
        available_models = [model.name for model in response]
        tts_models = [model for model in available_models if "tts" in model.lower()]
        
        if not tts_models:
            raise InvalidAPIKey("No TTS models available with this API key")
            
    except Exception as err:
        _LOGGER.error("Unable to connect to Gemini API: %s", err)
        raise CannotConnect from err

    return {"title": data.get(CONF_NAME, "Gemini AI TTS")}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Gemini AI TTS/STT."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAPIKey:
                errors["base"] = "invalid_api_key"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Gemini AI TTS/STT."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_MODEL,
                    default=self.config_entry.options.get(CONF_MODEL, DEFAULT_MODEL_TTS),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=k, label=v) 
                            for k, v in MODELS.items()
                        ]
                    )
                ),
                vol.Optional(
                    CONF_VOICE,
                    default=self.config_entry.options.get(CONF_VOICE, DEFAULT_VOICE),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=k, label=f"{k} ({v})") 
                            for k, v in VOICES.items()
                        ]
                    )
                ),
                vol.Optional(
                    CONF_STYLE,
                    default=self.config_entry.options.get(CONF_STYLE, DEFAULT_STYLE),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=SPEECH_STYLES)
                ),
                vol.Optional(
                    CONF_EMOTION,
                    default=self.config_entry.options.get(CONF_EMOTION, "neutral"),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=EMOTIONS)
                ),
                vol.Optional(
                    CONF_PACE,
                    default=self.config_entry.options.get(CONF_PACE, "normal"),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=PACE_OPTIONS)
                ),
                vol.Optional(
                    CONF_LANGUAGE,
                    default=self.config_entry.options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=k, label=v) 
                            for k, v in SUPPORTED_LANGUAGES.items()
                        ]
                    )
                ),
                vol.Optional(
                    CONF_STREAMING,
                    default=self.config_entry.options.get(CONF_STREAMING, DEFAULT_STREAMING),
                ): selector.BooleanSelector(),
                vol.Optional(
                    CONF_MULTI_SPEAKER,
                    default=self.config_entry.options.get(CONF_MULTI_SPEAKER, False),
                ): selector.BooleanSelector(),
                vol.Optional(
                    CONF_STT_LANGUAGE,
                    default=self.config_entry.options.get(CONF_STT_LANGUAGE, DEFAULT_STT_LANGUAGE),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=k, label=v) 
                            for k, v in STT_SUPPORTED_LANGUAGES.items()
                        ]
                    )
                ),
                vol.Optional(
                    CONF_STT_MODEL,
                    default=self.config_entry.options.get(CONF_STT_MODEL, DEFAULT_STT_MODEL),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value=k, label=v) 
                            for k, v in STT_MODELS.items()
                        ]
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAPIKey(HomeAssistantError):
    """Error to indicate the API key is invalid."""
