# Gemini AI TTS/STT Integration for Home Assistant

A comprehensive Home Assistant integration for Google Gemini AI with conversation agent capabilities and speech processing.

## ✅ **Current Status**

- **Text-to-Speech (TTS)** ✅ - **Fully functional** using native Gemini 2.5 Flash/Pro TTS
- **Conversation Agent** ✅ - Fully functional using Gemini 2.5 Pro
- **Speech-to-Text (STT)** ✅ - Fully functional using Google Cloud Speech-to-Text

## Features

### 🗣️ **Text-to-Speech (TTS)**
- **Native Gemini TTS** - Real speech synthesis using Gemini 2.5 Flash/Pro TTS models
- **30+ Premium Voices** - High-quality voices (Puck, Charon, Kore, Zephyr, etc.)
- **Advanced Voice Control** - Style, emotion, pace, and tone customization
- **Natural Language Prompts** - Control speech characteristics with natural instructions
- **Multi-language Support** - 24+ languages with automatic detection

### 🤖 **Conversation Agent** 
- **Gemini 2.5 Pro** - Advanced AI conversation with context and history
- **Configurable Parameters** - Temperature, max tokens, context length
- **Home Assistant Integration** - Native conversation entity

### 🎧 **Speech-to-Text (STT)**
- **Google Cloud Speech-to-Text** - Professional-grade recognition
- **60+ Languages** - Extensive language support
- **Advanced Models** - Optimized for different audio types
- **High Accuracy** - Professional speech recognition

> **Note**: STT functionality requires Google Cloud Speech-to-Text API credentials. This provides professional-grade speech recognition with high accuracy and extensive language support.

## Supported Models

### Text-to-Speech (TTS)
- `gemini-2.5-flash-preview-tts` - Fast, high-quality TTS (default)
- `gemini-2.5-pro-preview-tts` - Premium TTS with enhanced quality

### Conversation Agent
- `gemini-2.5-pro-preview-06-05` - Advanced conversation agent (default)
- `gemini-2.0-flash` - Fast conversation responses
- `gemini-1.5-pro` - Standard conversation model

### Speech-to-Text
- Google Cloud Speech-to-Text with multiple model options:
  - `latest_long` - Best for long audio (default)
  - `latest_short` - Best for short commands  
  - `command_and_search` - Optimized for voice commands
  - `phone_call` - Optimized for phone audio
  - `video` - Optimized for video audio

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Click "Add"
6. Find "Gemini AI TTS/STT" in the integration list
7. Click "Download"
8. Restart Home Assistant
9. Go to Configuration → Integrations
10. Click "Add Integration" and search for "Gemini AI TTS/STT"

### Manual Installation

1. Copy the `custom_components/gemini_ai_tts` folder to your `config/custom_components/` directory
2. Restart Home Assistant
3. Go to Configuration → Integrations
4. Click "Add Integration" and search for "Gemini AI TTS/STT"

## Configuration

### Required Settings

- **API Key**: Your Google AI API key (get one at https://ai.google.dev/)
- **Model**: Choose between available Gemini models

### STT Configuration (Optional)

For Speech-to-Text functionality, you'll also need:
- **Google Cloud Project ID**: Your Google Cloud project ID
- **Service Account Credentials**: JSON credentials for Google Cloud Speech-to-Text API

To set up STT:
1. Create a Google Cloud project at https://console.cloud.google.com/
2. Enable the Speech-to-Text API
3. Create a service account with Speech-to-Text permissions
4. Download the JSON credentials file
5. Copy the JSON content into the integration configuration

### Optional Settings

- **Voice**: Select from 30+ available voices
- **Speech Style**: Control tone, emotion, and delivery
- **Language**: Auto-detected or manually specified
- **Streaming**: Enable real-time audio streaming
- **Multi-speaker**: Configure multiple speakers for conversations

### Voice Options

The integration supports 30 different voices with various characteristics:

- **Bright**: Zephyr, Autonoe
- **Firm**: Kore, Orus, Alnilam  
- **Upbeat**: Puck, Laomedeia
- **Smooth**: Algieba, Despina
- **Informative**: Charon, Rasalgethi
- **And many more...**

## Usage

### Text-to-Speech Service

```yaml
service: tts.speak
data:
  entity_id: media_player.living_room
  message: "Hello, this is a test message"
  options:
    voice: "Puck"
    style: "cheerful"
```

### Conversation Agent

```yaml
service: conversation.process
data:
  text: "What's the weather like today?"
  agent_id: "gemini_ai_conversation"
```

### Advanced TTS with Emotion

```yaml
service: tts.speak
data:
  entity_id: media_player.bedroom
  message: "Say in a spooky whisper: Something wicked this way comes"
  options:
    voice: "Enceladus"
    emotion: "mysterious"
```

## Supported Languages

The integration supports 24 languages including:
- English (US, India)
- Spanish (US)
- French (France)
- German (Germany)
- Japanese (Japan)
- Korean (Korea)
- And many more...

## API Limits

- Context window: 32k tokens per session
- Input: Text only for TTS models
- Output: Audio only for TTS models
- Rate limits apply based on your Google AI API plan

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues:

1. Check the Home Assistant logs for error messages
2. Verify your API key is valid and has sufficient quota
3. Ensure you're using a supported Gemini model
4. Open an issue on GitHub with detailed information

## Changelog

### Version 1.0.0
- Initial release
- **Native Gemini TTS** with Gemini 2.5 Flash/Pro TTS models
- **30+ Premium Voices** with natural speech synthesis
- **Advanced Voice Control** - style, emotion, pace customization
- **Conversation Agent** with Gemini 2.5 Pro
- **Professional STT** with Google Cloud Speech-to-Text
- **Tabbed Configuration UI** for easy setup
- **Multi-language Support** - 24+ languages
