# Gemini AI TTS/STT Integration for Home Assistant

A comprehensive Home Assistant integration for Google Gemini Text-to-Speech (TTS) and Speech-to-Text (STT) with conversation agent capabilities.

## Features

- **Text-to-Speech (TTS)** using Gemini 2.5 Flash Preview TTS
- **Speech-to-Text (STT)** capabilities 
- **Conversation Agent** using Gemini 2.5 Pro Preview
- **30+ Voice Options** with different tones and styles
- **Multi-speaker support** for conversations
- **Streaming audio** for real-time responses
- **Configurable speech parameters** (tone, emotion, pace, accent)
- **Home Assistant native integration** with configuration UI

## Supported Models

- `gemini-2.5-flash-preview-tts` - Fast TTS generation
- `gemini-2.5-pro-preview-06-05` - Advanced conversation agent
- `gemini-2.5-pro-preview-tts` - High-quality TTS

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
- Basic TTS functionality with Gemini 2.5 Flash
- 30+ voice options
- Multi-speaker support
- Conversation agent integration
- Streaming audio support
- Configuration UI
