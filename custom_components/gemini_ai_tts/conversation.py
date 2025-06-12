"""Conversation agent for Gemini AI."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import google.generativeai as genai
from homeassistant.components.conversation import (
    ATTR_AGENT_ID,
    ConversationEntity,
    ConversationInput,
    ConversationResult,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import intent
from homeassistant.util import ulid

from .const import (
    DOMAIN,
    CONF_API_KEY,
    DEFAULT_MODEL_CONVERSATION,
    API_TIMEOUT,
    CONTEXT_WINDOW,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gemini AI Conversation platform via config entry."""
    api_key = config_entry.data[CONF_API_KEY]
    options = config_entry.options

    conversation_entity = GeminiConversationEntity(hass, api_key, options)
    async_add_entities([conversation_entity])


class GeminiConversationEntity(ConversationEntity):
    """Gemini AI Conversation entity."""

    def __init__(
        self, 
        hass: HomeAssistant, 
        api_key: str, 
        options: dict[str, Any]
    ) -> None:
        """Initialize the conversation entity."""
        self._hass = hass
        self._api_key = api_key
        self._options = options
        
        # Configure the client
        genai.configure(api_key=api_key)
        
        # Get model from options or use default
        model_name = options.get("conversation_model", DEFAULT_MODEL_CONVERSATION)
        self._model = genai.GenerativeModel(model_name)
        
        self._attr_name = "Gemini AI Conversation"
        self._attr_unique_id = f"{DOMAIN}_conversation"
        
        # Conversation history
        self._conversation_history: list[dict[str, str]] = []

    @property
    def supported_languages(self) -> list[str] | str:
        """Return a list of supported languages."""
        return [
            "ar",  # Arabic
            "en",  # English
            "es",  # Spanish
            "fr",  # French
            "de",  # German
            "hi",  # Hindi
            "id",  # Indonesian
            "it",  # Italian
            "ja",  # Japanese
            "ko",  # Korean
            "pt",  # Portuguese
            "ru",  # Russian
            "nl",  # Dutch
            "pl",  # Polish
            "th",  # Thai
            "tr",  # Turkish
            "vi",  # Vietnamese
            "ro",  # Romanian
            "uk",  # Ukrainian
            "bn",  # Bengali
            "mr",  # Marathi
            "ta",  # Tamil
            "te",  # Telugu
        ]

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        """Process a conversation turn."""
        try:
            response_text = await self._generate_response(user_input.text)
            
            # Add to conversation history
            self._conversation_history.append({
                "role": "user",
                "content": user_input.text
            })
            self._conversation_history.append({
                "role": "assistant", 
                "content": response_text
            })
            
            # Keep history manageable (last 20 exchanges)
            if len(self._conversation_history) > 40:
                self._conversation_history = self._conversation_history[-40:]
            
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_speech(response_text)
            
            return ConversationResult(
                response=intent_response,
                conversation_id=user_input.conversation_id or ulid.ulid(),
            )
            
        except Exception as err:
            _LOGGER.error("Error processing conversation: %s", err)
            
            intent_response = intent.IntentResponse(language=user_input.language)
            intent_response.async_set_error(
                intent.IntentResponseErrorCode.UNKNOWN,
                f"Sorry, I encountered an error: {err}",
            )
            
            return ConversationResult(
                response=intent_response,
                conversation_id=user_input.conversation_id,
            )

    async def _generate_response(self, user_message: str) -> str:
        """Generate a response using Gemini AI."""
        try:
            max_tokens = self._options.get("conversation_max_tokens", 1000)
            temperature = self._options.get("conversation_temperature", 0.7)
            context_length = self._options.get("conversation_context_length", 10)
            
            # Build conversation context
            messages = []
            
            # System message for Home Assistant context
            system_message = (
                "You are a helpful AI assistant integrated with Home Assistant. "
                "You can help users control their smart home devices, answer questions, "
                "and provide assistance with various tasks. Be conversational, helpful, "
                "and concise in your responses. If asked about specific Home Assistant "
                "entities or devices, provide relevant information based on the context."
            )
            
            messages.append(system_message)
            
            # Add conversation history (limited by context_length)
            history_limit = context_length * 2  # Each exchange has user + assistant
            for msg in self._conversation_history[-history_limit:]:
                if msg["role"] == "user":
                    messages.append(f"User: {msg['content']}")
                else:
                    messages.append(f"Assistant: {msg['content']}")
            
            # Add current user message
            messages.append(f"User: {user_message}")
            
            # Combine into a single prompt
            prompt = "\n".join(messages)
            
            # Ensure we don't exceed context window
            if len(prompt) > CONTEXT_WINDOW:
                # Truncate older conversation history
                prompt = system_message + "\n" + f"User: {user_message}"
            
            # Create generation config
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )
            
            # Generate response using the model
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._model.generate_content(
                    prompt,
                    generation_config=generation_config,
                ),
            )
            
            return response.text.strip()
            
        except Exception as err:
            _LOGGER.error("Error generating AI response: %s", err)
            raise

    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self._conversation_history.clear()
