# Development & Testing Guide

## Development Setup

### Prerequisites
- Home Assistant development environment
- Python 3.11 or higher
- Google AI API key from https://ai.google.dev/

### Installation for Development

1. Clone the repository:
```bash
git clone https://github.com/your-username/gemini-ai-tts.git
cd gemini-ai-tts
```

2. Create a symbolic link to your Home Assistant custom_components directory:
```bash
ln -s /path/to/gemini-ai-tts/custom_components/gemini_ai_tts /path/to/homeassistant/config/custom_components/
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Restart Home Assistant

### Testing the Integration

#### 1. Basic TTS Test
```yaml
# Test basic TTS functionality
service: tts.speak
data:
  entity_id: media_player.test_speaker
  message: "This is a test of Gemini TTS integration"
  options:
    voice: "Puck"
```

#### 2. Voice Quality Test
```yaml
# Test different voices
script:
  test_voice_quality:
    sequence:
      - repeat:
          for_each:
            - "Puck"
            - "Kore"
            - "Charon"
            - "Leda"
            - "Enceladus"
          sequence:
            - service: gemini_ai_tts.speak_with_style
              data:
                message: "Hello, this is voice {{ repeat.item }}. How do I sound?"
                entity_id: media_player.test_speaker
                voice: "{{ repeat.item }}"
            - delay: "00:00:05"
```

#### 3. Style and Emotion Test
```yaml
# Test different styles and emotions
script:
  test_styles_emotions:
    sequence:
      - service: gemini_ai_tts.speak_with_style
        data:
          message: "This is a cheerful and happy message!"
          entity_id: media_player.test_speaker
          voice: "Puck"
          style: "cheerful"
          emotion: "happy"
      - delay: "00:00:03"
      - service: gemini_ai_tts.speak_with_style
        data:
          message: "This is a mysterious and dramatic announcement"
          entity_id: media_player.test_speaker
          voice: "Enceladus"
          style: "dramatic"
          emotion: "mysterious"
      - delay: "00:00:03"
      - service: gemini_ai_tts.speak_with_style
        data:
          message: "This is a professional and serious statement"
          entity_id: media_player.test_speaker
          voice: "Charon"
          style: "professional"
          emotion: "serious"
```

#### 4. Multi-Speaker Test
```yaml
# Test multi-speaker functionality
service: gemini_ai_tts.speak_with_style
data:
  message: |
    Alice: Welcome to our smart home demo!
    Bob: Thanks Alice. Let's show off the multi-speaker capabilities.
    Alice: This technology is really impressive.
    Bob: I agree! The voices sound so natural.
  entity_id: media_player.test_speaker
  speakers:
    - "Alice" 
    - "Bob"
  voice: "Puck"
```

#### 5. Conversation Agent Test
```yaml
# Test conversation functionality
service: conversation.process
data:
  text: "What's the weather like today?"
  agent_id: "conversation.gemini_ai_conversation"
```

#### 6. Long Text Test
```yaml
# Test with longer content
service: gemini_ai_tts.speak_with_style
data:
  message: >
    This is a longer text to test how well the Gemini TTS integration handles
    extended content. We want to make sure that the voice quality remains
    consistent throughout the entire message, and that the pacing and
    intonation feel natural. This integration supports many different voices,
    each with their own unique characteristics and personality traits.
  entity_id: media_player.test_speaker
  voice: "Aoede"
  style: "natural"
  pace: "normal"
```

## Debugging

### Enable Debug Logging
Add to your `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.gemini_ai_tts: debug
    google.genai: debug
```

### Common Issues and Solutions

1. **API Key Invalid**
   - Verify your API key is correct
   - Check API key has proper permissions
   - Ensure you have quota remaining

2. **Audio Not Playing**
   - Check media player entity exists
   - Verify media player supports WAV format
   - Test with different media players

3. **Voice Not Found**
   - Check voice name spelling
   - Refer to supported voices list
   - Fallback to default voice

4. **Slow Response Times**
   - Check internet connection
   - Consider using streaming mode
   - Monitor API rate limits

## Performance Testing

### Latency Test
```python
import time
import asyncio
from homeassistant.core import HomeAssistant

async def test_tts_latency(hass: HomeAssistant):
    """Test TTS generation latency."""
    start_time = time.time()
    
    await hass.services.async_call(
        "gemini_ai_tts",
        "speak_with_style", 
        {
            "message": "This is a latency test",
            "entity_id": "media_player.test",
            "voice": "Puck"
        }
    )
    
    end_time = time.time()
    latency = end_time - start_time
    print(f"TTS Latency: {latency:.2f} seconds")
```

### Memory Usage Test
Monitor memory usage during extended TTS operations:
```bash
# Monitor Home Assistant process memory
ps aux | grep "hass"
```

## Contributing

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all functions
- Include error handling

### Testing Checklist
- [ ] Basic TTS functionality works
- [ ] All 30 voices are available
- [ ] Style and emotion options work
- [ ] Multi-speaker conversations work
- [ ] Conversation agent responds correctly
- [ ] Configuration flow works
- [ ] Options flow updates settings
- [ ] Services are registered properly
- [ ] Error handling works correctly
- [ ] No memory leaks during extended use

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit pull request with clear description

## Advanced Testing

### Load Testing
```yaml
# Test multiple concurrent TTS requests
script:
  load_test_tts:
    sequence:
      - repeat:
          count: 10
          sequence:
            - service: gemini_ai_tts.speak_with_style
              data:
                message: "Load test message {{ repeat.index }}"
                entity_id: "media_player.test_{{ repeat.index % 3 + 1 }}"
                voice: "{{ ['Puck', 'Kore', 'Charon'][repeat.index % 3] }}"
            - delay: "00:00:01"
```

### Integration Testing
```yaml
# Test integration with other Home Assistant components
automation:
  - trigger:
      platform: state
      entity_id: sensor.test_sensor
    action:
      - service: gemini_ai_tts.speak_with_style
        data:
          message: "Sensor value changed to {{ states('sensor.test_sensor') }}"
          entity_id: media_player.test_speaker
          voice: "Puck"
```

### Error Simulation
```yaml
# Test error handling
script:
  test_error_handling:
    sequence:
      # Test with invalid voice
      - service: gemini_ai_tts.speak_with_style
        data:
          message: "Testing invalid voice"
          entity_id: media_player.test_speaker
          voice: "InvalidVoice"
      # Test with very long message
      - service: gemini_ai_tts.speak_with_style
        data:
          message: "{{ 'Very long message. ' * 1000 }}"
          entity_id: media_player.test_speaker
          voice: "Puck"
```

## Documentation Updates

When making changes, ensure to update:
- README.md
- Configuration examples
- Service documentation  
- Voice options list
- Supported languages list
- API documentation
