"""Services for Gemini AI TTS/STT integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_VOICE,
    CONF_STYLE,
    CONF_EMOTION,
    CONF_PACE,
    VOICES,
    SPEECH_STYLES,
    EMOTIONS,
    PACE_OPTIONS,
)

_LOGGER = logging.getLogger(__name__)

SERVICE_SPEAK_WITH_STYLE = "speak_with_style"
SERVICE_CLEAR_CONVERSATION = "clear_conversation"
SERVICE_SET_DEFAULT_VOICE = "set_default_voice"

SPEAK_WITH_STYLE_SCHEMA = vol.Schema(
    {
        vol.Required("message"): cv.string,
        vol.Required("entity_id"): cv.entity_id,
        vol.Optional(CONF_VOICE): vol.In(list(VOICES.keys())),
        vol.Optional(CONF_STYLE): vol.In(SPEECH_STYLES),
        vol.Optional(CONF_EMOTION): vol.In(EMOTIONS),
        vol.Optional(CONF_PACE): vol.In(PACE_OPTIONS),
        vol.Optional("speakers"): vol.All(cv.ensure_list, [cv.string]),
    }
)

CLEAR_CONVERSATION_SCHEMA = vol.Schema(
    {
        vol.Optional("entity_id"): cv.entity_id,
    }
)

SET_DEFAULT_VOICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_VOICE): vol.In(list(VOICES.keys())),
        vol.Optional("entity_id"): cv.entity_id,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Gemini AI TTS/STT."""

    async def handle_speak_with_style(call: ServiceCall) -> None:
        """Handle speak with style service call."""
        message = call.data["message"]
        entity_id = call.data["entity_id"]
        voice = call.data.get(CONF_VOICE)
        style = call.data.get(CONF_STYLE)
        emotion = call.data.get(CONF_EMOTION)
        pace = call.data.get(CONF_PACE)
        speakers = call.data.get("speakers")

        # Build TTS options
        options = {}
        if voice:
            options["voice"] = voice
        if style:
            options["style"] = style
        if emotion:
            options["emotion"] = emotion
        if pace:
            options["pace"] = pace

        # Handle multi-speaker scenarios
        if speakers and len(speakers) > 1:
            # Format message for multi-speaker
            formatted_message = _format_multi_speaker_message(message, speakers)
            options["multi_speaker"] = True
            options["speakers"] = speakers
        else:
            formatted_message = message

        # Call TTS service
        await hass.services.async_call(
            "tts",
            "speak",
            {
                "entity_id": entity_id,
                "message": formatted_message,
                "options": options,
            },
        )

    async def handle_clear_conversation(call: ServiceCall) -> None:
        """Handle clear conversation service call."""
        entity_id = call.data.get("entity_id")
        
        # Find conversation entities
        if entity_id:
            entities = [entity_id]
        else:
            # Clear all Gemini conversation entities
            entities = [
                entity.entity_id
                for entity in hass.data.get(DOMAIN, {}).values()
                if hasattr(entity, "clear_conversation_history")
            ]

        for entity_id in entities:
            entity = hass.states.get(entity_id)
            if entity and hasattr(entity, "clear_conversation_history"):
                entity.clear_conversation_history()

    async def handle_set_default_voice(call: ServiceCall) -> None:
        """Handle set default voice service call."""
        voice = call.data[CONF_VOICE]
        entity_id = call.data.get("entity_id")
        
        # Update configuration for specified entity or all entities
        _LOGGER.info("Setting default voice to %s for entity %s", voice, entity_id or "all")
        
        # This would typically update the entity's configuration
        # Implementation depends on how you want to persist voice changes

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_SPEAK_WITH_STYLE,
        handle_speak_with_style,
        schema=SPEAK_WITH_STYLE_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CLEAR_CONVERSATION,
        handle_clear_conversation,
        schema=CLEAR_CONVERSATION_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_DEFAULT_VOICE,
        handle_set_default_voice,
        schema=SET_DEFAULT_VOICE_SCHEMA,
    )


def _format_multi_speaker_message(message: str, speakers: list[str]) -> str:
    """Format message for multi-speaker TTS."""
    if len(speakers) < 2:
        return message
    
    # Simple formatting - in practice, you might want more sophisticated parsing
    lines = message.split('\n')
    formatted_lines = []
    
    speaker_index = 0
    for line in lines:
        if ':' in line:
            # Line already has speaker format
            formatted_lines.append(line)
        else:
            # Add speaker to line
            speaker = speakers[speaker_index % len(speakers)]
            formatted_lines.append(f"{speaker}: {line}")
            speaker_index += 1
    
    return '\n'.join(formatted_lines)
