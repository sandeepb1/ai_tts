# 🎤 Gemini AI TTS/STT Integration - Technical Overview

## Architecture

This Home Assistant integration provides comprehensive Text-to-Speech (TTS), Speech-to-Text (STT), and Conversation Agent capabilities using Google's Gemini AI models.

### Core Components

1. **TTS Engine** (`tts.py`)
   - Supports 30+ unique voices with distinct characteristics
   - Advanced style control (cheerful, dramatic, whisper, etc.)
   - Emotion modulation (happy, serious, mysterious, etc.)
   - Pace control (very slow to very fast)
   - Multi-speaker conversations
   - Streaming audio support

2. **STT Engine** (`stt.py`)
   - Real-time speech transcription
   - 24 language support
   - Multiple audio format support (WAV, MP3, FLAC)
   - Configurable sample rates and bit rates

3. **Conversation Agent** (`conversation.py`)
   - Natural language conversation with Gemini 2.5 Pro
   - Context-aware responses
   - Integration with Home Assistant entities
   - Conversation history management

4. **Configuration System** (`config_flow.py`)
   - User-friendly setup wizard
   - Comprehensive options management
   - API key validation
   - Real-time configuration updates

### API Integration

#### Gemini Models Used
- **gemini-2.5-flash-preview-tts**: Fast TTS generation
- **gemini-2.5-pro-preview-tts**: High-quality TTS
- **gemini-2.5-pro-preview-06-05**: Conversation agent

#### Voice Characteristics
| Voice Category | Examples | Best For |
|---------------|----------|----------|
| Bright | Zephyr, Autonoe | Announcements, alerts |
| Firm | Kore, Orus, Alnilam | Professional content, instructions |
| Upbeat | Puck, Laomedeia | Welcome messages, positive content |
| Smooth | Algieba, Despina | Narration, storytelling |
| Informative | Charon, Rasalgethi | News, weather, factual content |
| Breathy | Enceladus | Intimate messages, bedtime stories |

### Advanced Features

#### Style Enhancement Engine
The integration automatically enhances messages with natural language instructions:

```python
# Input: "Welcome home!"
# Style: cheerful, Emotion: happy
# Enhanced: "Say cheerfully with happiness: Welcome home!"
```

#### Multi-Speaker Orchestration
Supports complex dialogue scenarios:
- Automatic speaker assignment
- Voice characteristic matching
- Conversation flow management

#### Context-Aware Conversations
The conversation agent maintains context and can:
- Reference previous exchanges
- Integrate with Home Assistant state
- Provide device-specific responses
- Handle multi-turn conversations

## Technical Specifications

### Audio Processing
- **Sample Rate**: 24kHz (configurable: 8kHz-48kHz)
- **Channels**: Mono/Stereo support
- **Bit Depth**: 16-bit
- **Format**: WAV (primary), MP3, FLAC supported
- **Latency**: ~2-5 seconds for standard requests

### Performance Characteristics
- **Concurrent Requests**: Supports multiple simultaneous TTS calls
- **Memory Usage**: ~50-100MB baseline, scales with request volume
- **Cache Strategy**: No local caching (cloud-based processing)
- **Rate Limits**: Managed by Google AI API quotas

### Error Handling
- Graceful API failure recovery
- Automatic voice fallback
- Request timeout management
- Detailed logging for troubleshooting

## Security & Privacy

### Data Handling
- API keys encrypted in Home Assistant configuration
- No audio data stored locally
- All processing occurs in Google's cloud
- Conversation history kept in memory only

### Network Requirements
- HTTPS connection to Google AI services
- Outbound port 443 access required
- Minimum 1Mbps bandwidth recommended for streaming

## Installation Methods

### HACS Installation (Recommended)
1. Add custom repository to HACS
2. Install integration
3. Restart Home Assistant
4. Configure via UI

### Manual Installation
1. Copy `custom_components/gemini_ai_tts/` to HA config
2. Install Python dependencies
3. Restart and configure

### Docker Considerations
- Ensure container has internet access
- Mount custom_components properly
- Consider resource limits for audio processing

## Configuration Examples

### Basic Setup
```yaml
# Minimal configuration
gemini_ai_tts:
  api_key: "your-api-key-here"
```

### Advanced Configuration
```yaml
# Full options configuration via UI:
# - Model: gemini-2.5-flash-preview-tts
# - Voice: Puck (Upbeat)
# - Style: Natural
# - Emotion: Neutral
# - Pace: Normal
# - Language: Auto-detect
# - Streaming: Enabled
# - Multi-speaker: Enabled
```

## Service APIs

### Core Services
- `tts.speak` - Standard TTS interface
- `gemini_ai_tts.speak_with_style` - Advanced TTS with full control
- `gemini_ai_tts.clear_conversation` - Reset conversation history
- `gemini_ai_tts.set_default_voice` - Update voice preferences

### Response Variables
```yaml
# Conversation responses include:
response_variable: gemini_response
# Access via: {{ gemini_response.response.speech.plain.speech }}
```

## Integration Points

### Home Assistant Entities
- Works with all media_player entities
- Integrates with input_text for conversation UI
- Supports automation triggers and conditions
- Compatible with scripts and scenes

### Voice Assistants
- Can be triggered by voice commands
- Integrates with Home Assistant voice pipeline
- Supports wake word detection flows

### External Systems
- REST API access via Home Assistant
- WebSocket real-time communication
- MQTT integration possible via automation

## Monitoring & Diagnostics

### Built-in Monitoring
- API call success/failure rates
- Response time tracking
- Error categorization
- Usage statistics

### Debug Information
```yaml
logger:
  logs:
    custom_components.gemini_ai_tts: debug
    google.genai: info
```

### Health Checks
- API connectivity validation
- Service availability monitoring
- Configuration validation
- Performance metrics

## Extension Points

### Custom Voice Profiles
Future support for:
- User voice training
- Custom voice models
- Voice cloning capabilities

### Advanced Audio Processing
Potential enhancements:
- Local audio caching
- Audio effect processing
- Real-time voice modulation

### AI Model Integration
Expandable to support:
- Multiple AI providers
- Local AI models
- Specialized voice models

## Troubleshooting Guide

### Common Issues
1. **No Audio Output**: Check media player compatibility
2. **Slow Responses**: Verify internet bandwidth
3. **Voice Not Available**: Check spelling, use voice list
4. **API Errors**: Validate key and quota
5. **Configuration Issues**: Review logs, check syntax

### Performance Optimization
- Use streaming for real-time applications
- Cache frequently used phrases (manual implementation)
- Batch multiple requests when possible
- Monitor API quota usage

### Development Tips
- Test with various media players
- Implement graceful degradation
- Use appropriate error handling
- Monitor resource usage
- Follow Home Assistant best practices

This integration represents a comprehensive solution for advanced speech synthesis and conversation capabilities in smart home environments, leveraging cutting-edge AI technology while maintaining ease of use and reliability.
