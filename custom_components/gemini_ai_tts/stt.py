"""Speech-to-Text platform for Gemini AI STT."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, AsyncGenerator

from google import genai
from google.genai import types
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

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_MODEL,
    CONF_LANGUAGE,
    DEFAULT_LANGUAGE,
    API_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gemini AI STT platform via config entry."""
    api_key = config_entry.data[CONF_API_KEY]
    options = config_entry.options

    stt_entity = GeminiSTTEntity(hass, api_key, options)
    async_add_entities([stt_entity])


class GeminiSTTEntity(SpeechToTextEntity):
    """Gemini AI Speech-to-Text entity."""

    def __init__(
        self, 
        hass: HomeAssistant, 
        api_key: str, 
        options: dict[str, Any]
    ) -> None:
        """Initialize the STT entity."""
        self._hass = hass
        self._api_key = api_key
        self._options = options
        self._client = genai.Client(api_key=api_key)
        
        self._attr_name = "Gemini AI STT"
        self._attr_unique_id = f"{DOMAIN}_stt"

    @property
    def supported_languages(self) -> list[str]:
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

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV, AudioFormats.MP3, AudioFormats.FLAC]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM, AudioCodecs.MP3, AudioCodecs.FLAC]

    @property
    def supported_bit_rates(self) -> list[AudioBitRates]:
        """Return a list of supported bit rates."""
        return [AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self) -> list[AudioSampleRates]:
        """Return a list of supported sample rates."""
        return [
            AudioSampleRates.SAMPLERATE_8000,
            AudioSampleRates.SAMPLERATE_16000,
            AudioSampleRates.SAMPLERATE_22050,
            AudioSampleRates.SAMPLERATE_24000,
            AudioSampleRates.SAMPLERATE_44100,
            AudioSampleRates.SAMPLERATE_48000,
        ]

    @property
    def supported_channels(self) -> list[AudioChannels]:
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO, AudioChannels.CHANNEL_STEREO]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: AsyncGenerator[bytes, None]
    ) -> SpeechResult:
        """Process an audio stream to STT."""
        try:
            # Collect audio data from stream
            audio_data = b""
            async for chunk in stream:
                audio_data += chunk

            if not audio_data:
                return SpeechResult(
                    text="",
                    result=SpeechResultState.ERROR,
                )

            # Process with Gemini
            text = await self._transcribe_audio(audio_data, metadata)
            
            if text:
                return SpeechResult(
                    text=text,
                    result=SpeechResultState.SUCCESS,
                )
            else:
                return SpeechResult(
                    text="",
                    result=SpeechResultState.ERROR,
                )

        except Exception as err:
            _LOGGER.error("Error processing audio stream: %s", err)
            return SpeechResult(
                text="",
                result=SpeechResultState.ERROR,
            )

    async def _transcribe_audio(
        self, audio_data: bytes, metadata: SpeechMetadata
    ) -> str:
        """Transcribe audio using Gemini API."""
        try:
            # Convert audio to format expected by Gemini
            # Note: This is a simplified implementation
            # In practice, you might need to handle different audio formats
            
            # Create the audio blob
            audio_blob = types.Blob(
                mime_type="audio/wav",
                data=audio_data
            )
            
            # Use a text model for audio transcription
            # Note: Gemini models with audio input capabilities
            model = "gemini-2.0-flash"
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._client.models.generate_content(
                    model=model,
                    contents=[
                        "Please transcribe the following audio to text:",
                        audio_blob
                    ],
                ),
            )
            
            return response.text.strip()
            
        except Exception as err:
            _LOGGER.error("Error transcribing audio: %s", err)
            raise
