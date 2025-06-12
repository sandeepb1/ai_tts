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
    CONF_STT_PROJECT_ID,
    CONF_STT_CREDENTIALS_JSON,
    CONF_STT_LANGUAGE,
    CONF_STT_MODEL,
    DEFAULT_MODEL_TTS,
    DEFAULT_MODEL_CONVERSATION,
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
    
    # Simple validation - just check if API key format is valid
    try:
        api_key = data[CONF_API_KEY]
        if not api_key or len(api_key) < 10:
            raise InvalidAPIKey("Invalid API key format")
        
        # For now, just validate the format instead of making actual API calls
        # The actual validation will happen when the service is used
        _LOGGER.info("API key format validation passed")
            
    except Exception as err:
        _LOGGER.error("Unable to validate API key: %s", err)
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
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Gemini AI TTS/STT."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    def _clean_config_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Clean config data to ensure it's JSON serializable."""
        clean_data = {}
        for key, value in data.items():
            if value is None:
                continue
            # Ensure value is JSON serializable
            try:
                import json
                json.dumps(value)
                clean_data[key] = value
            except (TypeError, ValueError):
                _LOGGER.warning("Skipping non-serializable config value for key %s", key)
        return clean_data

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options - show menu."""
        try:
            if user_input is not None:
                if user_input["next_step"] == "conversation":
                    return await self.async_step_conversation()
                elif user_input["next_step"] == "tts":
                    return await self.async_step_tts()
                elif user_input["next_step"] == "stt":
                    return await self.async_step_stt()
                else:
                    return await self.async_step_global()

            menu_schema = vol.Schema(
                {
                    vol.Required("next_step", default="global"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(value="global", label="Global Settings"),
                                selector.SelectOptionDict(value="conversation", label="Conversation Agent"),
                                selector.SelectOptionDict(value="tts", label="Text-to-Speech"),
                                selector.SelectOptionDict(value="stt", label="Speech-to-Text"),
                            ]
                        )
                    ),
                }
            )

            return self.async_show_form(
                step_id="init",
                data_schema=menu_schema,
                description_placeholders={
                    "title": "Configure Gemini AI TTS/STT",
                    "description": "Choose which component to configure"
                },
            )
        except Exception as err:
            _LOGGER.error("Error in options flow init: %s", err, exc_info=True)
            return self.async_abort(reason="unknown_error")

    async def async_step_global(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle global settings."""
        errors = {}
        
        if user_input is not None:
            try:
                # Safely validate and filter input data
                validated_input = {}
                allowed_keys = {CONF_LANGUAGE, CONF_STREAMING}
                
                for key, value in user_input.items():
                    if key in allowed_keys and value is not None:
                        validated_input[key] = value
                
                # Safely merge with existing options
                current_options = dict(self.config_entry.options) if self.config_entry.options else {}
                current_options.update(validated_input)
                
                # Ensure all data is JSON serializable
                clean_options = self._clean_config_data(current_options)
                
                return self.async_create_entry(title="", data=clean_options)
                
            except Exception as err:
                _LOGGER.error("Error saving global settings: %s", err, exc_info=True)
                errors["base"] = "unknown_error"

        try:
            global_schema = vol.Schema(
                {
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
                }
            )

            return self.async_show_form(
                step_id="global",
                data_schema=global_schema,
                errors=errors,
                description_placeholders={
                    "title": "Global Settings",
                    "description": "Configure global settings that apply to all components"
                },
            )
        except Exception as err:
            _LOGGER.error("Error creating global config form: %s", err, exc_info=True)
            return self.async_abort(reason="unknown_error")

    async def async_step_conversation(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle conversation agent configuration."""
        errors = {}
        
        if user_input is not None:
            try:
                # Safely validate and filter input data
                validated_input = {}
                allowed_keys = {"conversation_model", "conversation_max_tokens", 
                              "conversation_temperature", "conversation_context_length"}
                
                for key, value in user_input.items():
                    if key in allowed_keys and value is not None:
                        validated_input[key] = value
                
                # Safely merge with existing options
                current_options = dict(self.config_entry.options) if self.config_entry.options else {}
                current_options.update(validated_input)
                
                # Ensure all data is JSON serializable
                clean_options = self._clean_config_data(current_options)
                
                return self.async_create_entry(title="", data=clean_options)
                
            except Exception as err:
                _LOGGER.error("Error saving conversation settings: %s", err, exc_info=True)
                errors["base"] = "unknown_error"

        try:
            # Filter models for conversation
            conversation_models = {
                k: v for k, v in MODELS.items() 
                if "conversation" in v.lower() or "pro" in v.lower()
            }

            conversation_schema = vol.Schema(
                {
                    vol.Optional(
                        "conversation_model",
                        default=self.config_entry.options.get("conversation_model", DEFAULT_MODEL_CONVERSATION),
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(value=k, label=v) 
                                for k, v in conversation_models.items()
                            ]
                        )
                    ),
                    vol.Optional(
                        "conversation_temperature",
                        default=self.config_entry.options.get("conversation_temperature", 0.7),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=0.0,
                            max=2.0,
                            step=0.1,
                            mode=selector.NumberSelectorMode.SLIDER,
                        )
                    ),
                    vol.Optional(
                        "conversation_max_tokens",
                        default=self.config_entry.options.get("conversation_max_tokens", 1000),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=100,
                            max=4000,
                            step=100,
                            mode=selector.NumberSelectorMode.BOX,
                        )
                    ),
                    vol.Optional(
                        "conversation_context_length",
                        default=self.config_entry.options.get("conversation_context_length", 10),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=50,
                            step=1,
                            mode=selector.NumberSelectorMode.BOX,
                        )
                    ),
                }
            )

            return self.async_show_form(
                step_id="conversation",
                data_schema=conversation_schema,
                errors=errors,
                description_placeholders={
                    "title": "Conversation Agent Settings",
                    "description": "Configure the AI conversation agent powered by Gemini Pro"
                },
            )
        except Exception as err:
            _LOGGER.error("Error creating conversation config form: %s", err, exc_info=True)
            return self.async_abort(reason="unknown_error")

    async def async_step_tts(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle TTS configuration."""
        errors = {}
        
        if user_input is not None:
            try:
                # Safely validate and filter input data
                validated_input = {}
                allowed_keys = {"tts_model", CONF_VOICE, CONF_STYLE, CONF_EMOTION, CONF_PACE, "tts_quality"}
                
                for key, value in user_input.items():
                    if key in allowed_keys and value is not None:
                        validated_input[key] = value
                
                # Safely merge with existing options
                current_options = dict(self.config_entry.options) if self.config_entry.options else {}
                current_options.update(validated_input)
                
                # Ensure all data is JSON serializable
                clean_options = self._clean_config_data(current_options)
                
                return self.async_create_entry(title="", data=clean_options)
                
            except Exception as err:
                _LOGGER.error("Error saving TTS settings: %s", err, exc_info=True)
                errors["base"] = "unknown_error"

        try:
            # Filter models for TTS
            tts_models = {
                k: v for k, v in MODELS.items() 
                if "tts" in v.lower()
            }

            tts_schema = vol.Schema(
                {
                    vol.Optional(
                        "tts_model",
                        default=self.config_entry.options.get("tts_model", DEFAULT_MODEL_TTS),
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(value=k, label=v) 
                                for k, v in tts_models.items()
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
                        "tts_quality",
                        default=self.config_entry.options.get("tts_quality", "standard"),
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(value="standard", label="Standard Quality"),
                                selector.SelectOptionDict(value="high", label="High Quality"),
                            ]
                        )
                    ),
                }
            )

            return self.async_show_form(
                step_id="tts",
                data_schema=tts_schema,
                errors=errors,
                description_placeholders={
                    "title": "Text-to-Speech Settings",
                    "description": "Configure voice synthesis options and speech characteristics"
                },
            )
        except Exception as err:
            _LOGGER.error("Error creating TTS config form: %s", err, exc_info=True)
            return self.async_abort(reason="unknown_error")

    async def async_step_stt(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle STT configuration."""
        errors = {}
        
        if user_input is not None:
            try:
                # Safely validate and filter input data
                validated_input = {}
                allowed_keys = {
                    CONF_STT_LANGUAGE, CONF_STT_MODEL, "stt_enhanced_models",
                    "stt_profanity_filter", "stt_enable_word_confidence",
                    "stt_enable_automatic_punctuation", "stt_sample_rate"
                }
                
                for key, value in user_input.items():
                    if key in allowed_keys and value is not None:
                        validated_input[key] = value
                
                # Safely merge with existing options
                current_options = dict(self.config_entry.options) if self.config_entry.options else {}
                current_options.update(validated_input)
                
                # Ensure all data is JSON serializable
                clean_options = self._clean_config_data(current_options)
                
                return self.async_create_entry(title="", data=clean_options)
                
            except Exception as err:
                _LOGGER.error("Error saving STT settings: %s", err, exc_info=True)
                errors["base"] = "unknown_error"

        try:
            stt_schema = vol.Schema(
                {
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
                    vol.Optional(
                        "stt_enhanced_models",
                        default=self.config_entry.options.get("stt_enhanced_models", True),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        "stt_profanity_filter",
                        default=self.config_entry.options.get("stt_profanity_filter", False),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        "stt_enable_word_confidence",
                        default=self.config_entry.options.get("stt_enable_word_confidence", False),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        "stt_enable_automatic_punctuation",
                        default=self.config_entry.options.get("stt_enable_automatic_punctuation", True),
                    ): selector.BooleanSelector(),
                    vol.Optional(
                        "stt_sample_rate",
                        default=self.config_entry.options.get("stt_sample_rate", "16000"),
                    ): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(value="8000", label="8 kHz"),
                                selector.SelectOptionDict(value="16000", label="16 kHz (Recommended)"),
                                selector.SelectOptionDict(value="22050", label="22.05 kHz"),
                                selector.SelectOptionDict(value="24000", label="24 kHz"),
                                selector.SelectOptionDict(value="44100", label="44.1 kHz"),
                                selector.SelectOptionDict(value="48000", label="48 kHz"),
                            ]
                        )
                    ),
                }
            )

            return self.async_show_form(
                step_id="stt",
                data_schema=stt_schema,
                errors=errors,
                description_placeholders={
                    "title": "Speech-to-Text Settings",
                    "description": "Configure speech recognition options and language settings"
                },
            )
        except Exception as err:
            _LOGGER.error("Error creating STT config form: %s", err, exc_info=True)
            return self.async_abort(reason="unknown_error")


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAPIKey(HomeAssistantError):
    """Error to indicate the API key is invalid."""
