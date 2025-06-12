# Gemini AI TTS/STT Integration - Usage Examples

## Basic TTS Usage

### Simple Text-to-Speech
```yaml
service: tts.speak
data:
  entity_id: media_player.living_room
  message: "Hello, this is a test of Gemini TTS"
  options:
    voice: "Puck"
```

### Advanced TTS with Style
```yaml
service: gemini_ai_tts.speak_with_style
data:
  message: "Welcome home! I hope you had a wonderful day."
  entity_id: media_player.living_room_speaker
  voice: "Puck"
  style: "cheerful"
  emotion: "happy"
  pace: "normal"
```

## Multi-Speaker Conversations

### Two-Speaker Dialogue
```yaml
service: gemini_ai_tts.speak_with_style
data:
  message: |
    Alice: How are you today?
    Bob: I'm doing great, thanks for asking!
    Alice: That's wonderful to hear.
  entity_id: media_player.living_room
  speakers:
    - "Alice"
    - "Bob"
  voice: "Puck"
```

## Conversation Agent Usage

### Basic Conversation
```yaml
service: conversation.process
data:
  text: "What's the weather like today?"
  agent_id: "conversation.gemini_ai_conversation"
```

### Automation with Conversation Response
```yaml
automation:
  - trigger:
      platform: voice
      command: "Ask Gemini about the weather"
    action:
      - service: conversation.process
        data:
          text: "What's today's weather forecast?"
          agent_id: "conversation.gemini_ai_conversation"
        response_variable: response
      - service: tts.speak
        data:
          entity_id: media_player.kitchen
          message: "{{ response.response.speech.plain.speech }}"
```

## Voice Options

### All Available Voices
```yaml
# Bright voices
- Zephyr (Bright)
- Autonoe (Bright)

# Firm voices  
- Kore (Firm)
- Orus (Firm)
- Alnilam (Firm)

# Upbeat voices
- Puck (Upbeat)
- Laomedeia (Upbeat)

# Smooth voices
- Algieba (Smooth)
- Despina (Smooth)

# Informative voices
- Charon (Informative)
- Rasalgethi (Informative)

# And many more...
```

### Voice Comparison Script
```yaml
script:
  compare_voices:
    sequence:
      - variables:
          test_message: "This is a test of the voice capabilities"
          voices:
            - "Puck"
            - "Kore" 
            - "Charon"
            - "Leda"
            - "Enceladus"
      - repeat:
          for_each: "{{ voices }}"
          sequence:
            - service: gemini_ai_tts.speak_with_style
              data:
                message: "{{ test_message }} using voice {{ repeat.item }}"
                entity_id: media_player.living_room
                voice: "{{ repeat.item }}"
            - delay: "00:00:03"
```

## Emotional Expressions

### Different Emotions
```yaml
# Happy announcement
service: gemini_ai_tts.speak_with_style
data:
  message: "Congratulations! The task was completed successfully!"
  voice: "Puck"
  emotion: "happy"
  style: "excited"

# Calm reminder
service: gemini_ai_tts.speak_with_style
data:
  message: "Please remember to lock the doors before going to bed"
  voice: "Charon"
  emotion: "calm"
  style: "professional"

# Mysterious announcement
service: gemini_ai_tts.speak_with_style
data:
  message: "Something unusual has been detected in the basement"
  voice: "Enceladus"
  emotion: "mysterious"
  style: "whisper"
```

## Integration with Home Assistant Features

### Smart Home Announcements
```yaml
automation:
  # Door lock status
  - trigger:
      platform: state
      entity_id: lock.front_door
      to: "locked"
    action:
      service: gemini_ai_tts.speak_with_style
      data:
        message: "Front door is now securely locked"
        entity_id: media_player.hallway
        voice: "Kore"
        style: "confident"
        emotion: "serious"

  # Temperature alerts
  - trigger:
      platform: numeric_state
      entity_id: sensor.outdoor_temperature
      above: 85
    action:
      service: gemini_ai_tts.speak_with_style
      data:
        message: "It's getting quite warm outside. The temperature is {{ states('sensor.outdoor_temperature') }} degrees."
        entity_id: media_player.whole_house
        voice: "Aoede"
        style: "friendly"
        emotion: "neutral"
```

### Dynamic Content
```yaml
automation:
  - trigger:
      platform: time
      at: "08:00:00"
    action:
      service: gemini_ai_tts.speak_with_style
      data:
        message: >
          Good morning! Today is {{ now().strftime('%A, %B %d') }}.
          The weather is {{ states('weather.home') }} with a temperature of {{ state_attr('weather.home', 'temperature') }} degrees.
          You have {{ states('calendar.personal') | length }} events scheduled for today.
        entity_id: media_player.bedroom
        voice: "Leda"
        style: "cheerful"
        emotion: "happy"
```

## Service Management

### Clear Conversation History
```yaml
service: gemini_ai_tts.clear_conversation
# Clears conversation history for all Gemini conversation agents
```

### Set Default Voice
```yaml
service: gemini_ai_tts.set_default_voice
data:
  voice: "Puck"
  # Sets Puck as the default voice for all TTS entities
```

## Advanced Configurations

### Language-Specific Announcements
```yaml
automation:
  - trigger:
      platform: state
      entity_id: input_select.house_language
    action:
      - choose:
          - conditions:
              condition: state
              entity_id: input_select.house_language
              state: "Spanish"
            sequence:
              service: gemini_ai_tts.speak_with_style
              data:
                message: "Bienvenido a casa"
                language: "es-US"
                voice: "Puck"
          - conditions:
              condition: state
              entity_id: input_select.house_language
              state: "French"
            sequence:
              service: gemini_ai_tts.speak_with_style
              data:
                message: "Bienvenue à la maison"
                language: "fr-FR"
                voice: "Aoede"
```

### Conditional Voice Selection
```yaml
automation:
  - trigger:
      platform: time
      at: "06:00:00"
    action:
      service: gemini_ai_tts.speak_with_style
      data:
        message: "Good morning! Time to start the day."
        entity_id: media_player.bedroom
        voice: >
          {% if is_state('input_boolean.weekend_mode', 'on') %}
            Leda
          {% else %}
            Charon
          {% endif %}
        style: >
          {% if is_state('input_boolean.weekend_mode', 'on') %}
            calm
          {% else %}
            professional
          {% endif %}
```
