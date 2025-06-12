"""Speech-to-Text platform for Gemini AI STT using Google Cloud Speech-to-Text."""
from __future__ import annotations

import asyncio
import io
import json
import logging
import os
import tempfile
from typing import Any, AsyncGenerator

from google.cloud import speech
from google.oauth2 import service_account
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
    CONF_STT_PROJECT_ID,
    CONF_STT_CREDENTIALS_JSON,
    CONF_STT_LANGUAGE,
    CONF_STT_MODEL,
    DEFAULT_STT_LANGUAGE,
    DEFAULT_STT_MODEL,
    API_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Gemini AI STT platform via config entry."""
    config_data = config_entry.data
    options = config_entry.options

    # Check if STT is configured
    project_id = config_data.get(CONF_STT_PROJECT_ID)
    credentials_json = config_data.get(CONF_STT_CREDENTIALS_JSON)
    
    if not project_id or not credentials_json:
        _LOGGER.warning(
            "STT not configured. Please provide Google Cloud project ID and credentials."
        )
        return

    try:
        stt_entity = GeminiSTTEntity(hass, config_data, options)
        async_add_entities([stt_entity])
    except Exception as err:
        _LOGGER.error("Failed to set up STT entity: %s", err)


class GeminiSTTEntity(SpeechToTextEntity):
    """Gemini AI Speech-to-Text entity using Google Cloud Speech-to-Text."""

    def __init__(
        self, 
        hass: HomeAssistant, 
        config_data: dict[str, Any],
        options: dict[str, Any]
    ) -> None:
        """Initialize the STT entity."""
        self._hass = hass
        self._config_data = config_data
        self._options = options
        
        self._attr_name = "Gemini AI STT"
        self._attr_unique_id = f"{DOMAIN}_stt"
        
        # Initialize Google Cloud Speech client
        self._client = None
        self._setup_client()

    def _setup_client(self) -> None:
        """Set up Google Cloud Speech client."""
        try:
            project_id = self._config_data.get(CONF_STT_PROJECT_ID)
            credentials_json = self._config_data.get(CONF_STT_CREDENTIALS_JSON)
            
            if not project_id or not credentials_json:
                _LOGGER.error("STT configuration missing project ID or credentials")
                return
                
            # Parse credentials JSON
            try:
                credentials_dict = json.loads(credentials_json)
            except json.JSONDecodeError as err:
                _LOGGER.error("Invalid credentials JSON: %s", err)
                return
                
            # Create credentials object
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict
            )
            
            # Create client
            self._client = speech.SpeechClient(credentials=credentials)
            _LOGGER.info("Google Cloud Speech client initialized successfully")
            
        except Exception as err:
            _LOGGER.error("Failed to setup Google Cloud Speech client: %s", err)
            self._client = None

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return [
            "ar",  # Arabic
            "bg",  # Bulgarian
            "ca",  # Catalan
            "cs",  # Czech
            "da",  # Danish
            "de",  # German
            "el",  # Greek
            "en",  # English
            "es",  # Spanish
            "et",  # Estonian
            "fi",  # Finnish
            "fr",  # French
            "he",  # Hebrew
            "hi",  # Hindi
            "hr",  # Croatian
            "hu",  # Hungarian
            "id",  # Indonesian
            "is",  # Icelandic
            "it",  # Italian
            "ja",  # Japanese
            "ko",  # Korean
            "lt",  # Lithuanian
            "lv",  # Latvian
            "ms",  # Malay
            "nl",  # Dutch
            "no",  # Norwegian
            "pl",  # Polish
            "pt",  # Portuguese
            "ro",  # Romanian
            "ru",  # Russian
            "sk",  # Slovak
            "sl",  # Slovenian
            "sv",  # Swedish
            "th",  # Thai
            "tr",  # Turkish
            "uk",  # Ukrainian
            "vi",  # Vietnamese
            "zh",  # Chinese
        ]

    @property
    def supported_formats(self) -> list[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self) -> list[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

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
        if not self._client:
            _LOGGER.error("Google Cloud Speech client not initialized")
            return SpeechResult(
                text="",
                result=SpeechResultState.ERROR,
            )

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

            # Process with Google Cloud Speech-to-Text
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
        """Transcribe audio using Google Cloud Speech-to-Text API."""
        try:
            if not self._client:
                raise Exception("Google Cloud Speech client not available")
                
            # Get language from options or use default
            language = self._options.get(CONF_STT_LANGUAGE, DEFAULT_STT_LANGUAGE)
            model = self._options.get(CONF_STT_MODEL, DEFAULT_STT_MODEL)
            
            # Prepare audio format configuration
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
            
            # Determine sample rate from metadata
            sample_rate = 16000  # Default
            if metadata.sample_rate:
                if metadata.sample_rate == AudioSampleRates.SAMPLERATE_8000:
                    sample_rate = 8000
                elif metadata.sample_rate == AudioSampleRates.SAMPLERATE_16000:
                    sample_rate = 16000
                elif metadata.sample_rate == AudioSampleRates.SAMPLERATE_22050:
                    sample_rate = 22050
                elif metadata.sample_rate == AudioSampleRates.SAMPLERATE_24000:
                    sample_rate = 24000
                elif metadata.sample_rate == AudioSampleRates.SAMPLERATE_44100:
                    sample_rate = 44100
                elif metadata.sample_rate == AudioSampleRates.SAMPLERATE_48000:
                    sample_rate = 48000
                    
            # Determine channel count
            audio_channel_count = 1
            if metadata.channel == AudioChannels.CHANNEL_STEREO:
                audio_channel_count = 2
                
            # Handle different audio formats
            if metadata.format == AudioFormats.OGG:
                if metadata.codec == AudioCodecs.OPUS:
                    encoding = speech.RecognitionConfig.AudioEncoding.OGG_OPUS
                else:
                    encoding = speech.RecognitionConfig.AudioEncoding.OGG_OPUS
            elif metadata.format == AudioFormats.WAV:
                encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
            
            # Create recognition config
            config = speech.RecognitionConfig(
                encoding=encoding,
                sample_rate_hertz=sample_rate,
                language_code=language,
                audio_channel_count=audio_channel_count,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=False,
                model=model,
                use_enhanced=True,
            )
            
            # Create audio object
            audio = speech.RecognitionAudio(content=audio_data)
            
            # Perform transcription
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self._client.recognize(config=config, audio=audio),
            )
            
            # Extract transcription
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                _LOGGER.debug("Transcription result: %s", transcript)
                return transcript.strip()
            else:
                _LOGGER.warning("No transcription results returned")
                return ""
                
        except Exception as err:
            _LOGGER.error("Error transcribing audio: %s", err)
            raise

    async def _streaming_transcribe_audio(
        self, audio_stream: AsyncGenerator[bytes, None], metadata: SpeechMetadata
    ) -> str:
        """Transcribe audio using streaming recognition (for future enhancement)."""
        # This method can be implemented for real-time streaming transcription
        # For now, we use the batch recognition method
        pass
