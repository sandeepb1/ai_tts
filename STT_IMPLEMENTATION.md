# STT Implementation Notes

## Current Status

The STT (Speech-to-Text) functionality in this integration is currently a **placeholder implementation**. This is because:

1. **Gemini Audio Input Limitations**: While Gemini models can process audio, the current audio input capabilities are still evolving and may not be suitable for real-time STT in Home Assistant.

2. **Home Assistant STT Requirements**: HA's STT framework has specific requirements for audio format handling that need careful implementation.

3. **Performance Considerations**: Real-time STT requires low latency and efficient processing.

## Recommended STT Solutions

For production use, consider these alternatives:

### 1. Google Cloud Speech-to-Text
```python
# Example implementation using Google Cloud STT
from google.cloud import speech

async def transcribe_with_google_stt(audio_data: bytes) -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""
```

### 2. OpenAI Whisper
```python
# Example using OpenAI Whisper API
import openai

async def transcribe_with_whisper(audio_data: bytes) -> str:
    response = await openai.Audio.atranscribe(
        model="whisper-1",
        file=io.BytesIO(audio_data),
        response_format="text"
    )
    return response
```

### 3. Azure Speech Services
```python
# Example using Azure Cognitive Services
import azure.cognitiveservices.speech as speechsdk

async def transcribe_with_azure(audio_data: bytes) -> str:
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    audio_config = speechsdk.audio.AudioConfig(stream=speechsdk.audio.PushAudioInputStream())
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    # Implementation details...
```

## Future Implementation Plan

To implement proper STT support:

1. **Choose STT Provider**: Select Google Cloud STT, Whisper, or Azure
2. **Update Dependencies**: Add required SDK to `manifest.json`
3. **Implement Audio Processing**: Handle different audio formats and sample rates
4. **Add Configuration**: Allow users to configure STT provider and settings
5. **Error Handling**: Implement robust error handling and fallbacks
6. **Testing**: Comprehensive testing with various audio inputs

## Enabling STT (When Ready)

When STT is properly implemented:

1. Uncomment the STT platform in `__init__.py`:
```python
PLATFORMS: list[Platform] = [
    Platform.TTS,
    Platform.STT,  # Enable when ready
    Platform.CONVERSATION,
]
```

2. Update `hacs.json` to include STT domain:
```json
"domains": ["tts", "stt", "conversation"]
```

3. Complete the STT implementation in `stt.py`

## Current Workaround

For immediate STT needs, users can:
1. Use Home Assistant's built-in STT providers
2. Set up Google Cloud STT as a separate integration
3. Use Rhasspy or other open-source STT solutions
4. Wait for this integration's STT implementation to be completed

The TTS and Conversation Agent features are fully functional and ready for production use.
