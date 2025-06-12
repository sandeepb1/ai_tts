"""Text-to-Speech platform for Gemini AI TTS."""
from __future__ import annotations

import asyncio
import io
import logging
import wave
from typing import Any

from google import genai
from google.genai import types
from homeassistant.components.tts import ATTR_VOICE, CONF_LANG, TextToSpeechEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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
    DEFAULT_MODEL_TTS,
    DEFAULT_VOICE,
    DEFAULT_STYLE,
    DEFAULT_LANGUAGE,
    VOICES,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_SAMPLE_WIDTH,
    API_TIMEOUT,
    MAX_TEXT_LENGTH,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gemini AI TTS platform via config entry."""
    api_key = config_entry.data[CONF_API_KEY]
    options = config_entry.options

    tts_entity = GeminiTTSEntity(hass, api_key, options)
    async_add_entities([tts_entity])


class GeminiTTSEntity(TextToSpeechEntity):
    """Gemini AI Text-to-Speech entity."""

    def __init__(
        self, 
        hass: HomeAssistant, 
        api_key: str, 
        options: dict[str, Any]
    ) -> None:
        """Initialize the TTS entity."""
        self._hass = hass
        self._api_key = api_key
        self._options = options
        
        # Initialize the Gemini client for TTS
        self._client = genai.Client(api_key=api_key)
        
        self._attr_name = "Gemini AI TTS"
        self._attr_unique_id = f"{DOMAIN}_tts"

    @property
    def default_language(self) -> str:
        """Return the default language."""
        return self._options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"]

    @property
    def supported_options(self) -> list[str]:
        """Return list of supported options."""
        return [
            ATTR_VOICE,
            CONF_STYLE,
            CONF_EMOTION,
            CONF_PACE,
            CONF_LANGUAGE,
            CONF_STREAMING,
        ]

    @property
    def default_options(self) -> dict[str, Any]:
        """Return dict of default options."""
        return {
            ATTR_VOICE: self._options.get(CONF_VOICE, DEFAULT_VOICE),
            CONF_STYLE: self._options.get(CONF_STYLE, DEFAULT_STYLE),
            CONF_EMOTION: self._options.get(CONF_EMOTION, "neutral"),
            CONF_PACE: self._options.get(CONF_PACE, "normal"),
            CONF_LANGUAGE: self._options.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
            CONF_STREAMING: self._options.get(CONF_STREAMING, True),
        }

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict[str, Any]
    ) -> tuple[str, bytes]:
        """Load TTS audio."""
        if len(message) > MAX_TEXT_LENGTH:
            _LOGGER.warning(
                "Message too long (%d chars). Truncating to %d chars.",
                len(message),
                MAX_TEXT_LENGTH,
            )
            message = message[:MAX_TEXT_LENGTH]

        voice = options.get(ATTR_VOICE, self.default_options[ATTR_VOICE])
        style = options.get(CONF_STYLE, self.default_options[CONF_STYLE])
        emotion = options.get(CONF_EMOTION, self.default_options[CONF_EMOTION])
        pace = options.get(CONF_PACE, self.default_options[CONF_PACE])
        
        # Enhance the message with style instructions
        enhanced_message = self._enhance_message_with_style(message, style, emotion, pace)
        
        try:
            audio_data = await self._generate_speech(enhanced_message, voice, options)
            return "wav", audio_data
        except Exception as err:
            _LOGGER.error("Error generating TTS audio: %s", err)
            raise

    def _enhance_message_with_style(
        self, message: str, style: str, emotion: str, pace: str
    ) -> str:
        """Enhance message with style, emotion, and pace instructions."""
        if style == "natural" and emotion == "neutral" and pace == "normal":
            return message
            
        instructions = []
        
        # Add style instruction
        if style != "natural":
            if style == "whisper":
                instructions.append("in a whisper")
            elif style == "dramatic":
                instructions.append("dramatically")
            elif style == "professional":
                instructions.append("in a professional tone")
            elif style == "friendly":
                instructions.append("in a friendly manner")
            elif style == "mysterious":
                instructions.append("mysteriously")
            elif style == "confident":
                instructions.append("confidently")
            else:
                instructions.append(f"in a {style} way")
        
        # Add emotion instruction
        if emotion != "neutral":
            if emotion == "happy":
                instructions.append("cheerfully")
            elif emotion == "excited":
                instructions.append("with excitement")
            elif emotion == "calm":
                instructions.append("calmly")
            elif emotion == "serious":
                instructions.append("seriously")
            else:
                instructions.append(f"with {emotion}")
        
        # Add pace instruction
        if pace != "normal":
            if pace == "very_slow":
                instructions.append("very slowly")
            elif pace == "slow":
                instructions.append("slowly")
            elif pace == "fast":
                instructions.append("quickly")
            elif pace == "very_fast":
                instructions.append("very quickly")
        
        if instructions:
            instruction_text = ", ".join(instructions)
            return f"Say {instruction_text}: {message}"
        
        return message

    async def _generate_speech(
        self, message: str, voice: str, options: dict[str, Any]
    ) -> bytes:
        """Generate speech using Gemini TTS API."""
        # Validate voice
        if voice not in VOICES:
            _LOGGER.warning("Invalid voice '%s', using default '%s'", voice, DEFAULT_VOICE)
            voice = DEFAULT_VOICE
            
        try:
            # Get model from options or use default
            model = self._options.get("tts_model", DEFAULT_MODEL_TTS)
            
            # Generate speech using the real Gemini TTS API
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._client.models.generate_content(
                    model=model,
                    contents=message,
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=voice,
                                )
                            )
                        ),
                    )
                ),
            )
            
            # Extract audio data from response
            if response.candidates and response.candidates[0].content.parts:
                audio_data = response.candidates[0].content.parts[0].inline_data.data
                
                # Convert to WAV format if needed
                return self._ensure_wav_format(audio_data)
            else:
                raise Exception("No audio data received from Gemini TTS API")
            
        except Exception as err:
            _LOGGER.error("Error generating speech with Gemini TTS: %s", err)
            raise

    def _ensure_wav_format(self, audio_data: bytes) -> bytes:
        """Ensure audio data is in WAV format."""
        try:
            # The Gemini TTS API returns raw PCM data at 24kHz, 16-bit, mono
            # We need to add a WAV header to make it a proper WAV file
            
            sample_rate = AUDIO_SAMPLE_RATE  # 24000 Hz as per Gemini docs
            channels = AUDIO_CHANNELS        # 1 (mono)
            sample_width = AUDIO_SAMPLE_WIDTH # 2 bytes (16-bit)
            
            # Create WAV file with proper header
            output = io.BytesIO()
            with wave.open(output, "wb") as wav_file:
                wav_file.setnchannels(channels)
                wav_file.setsampwidth(sample_width)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
            
            return output.getvalue()
            
        except Exception as err:
            _LOGGER.error("Error formatting audio as WAV: %s", err)
            # Return original data if formatting fails
            return audio_data
