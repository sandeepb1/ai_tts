# 🎙️ Speech-to-Text (STT) Setup Guide

## Overview

The Gemini AI TTS/STT integration now includes full **Speech-to-Text functionality** powered by Google Cloud Speech-to-Text API. This provides professional-grade speech recognition with:

- **60+ languages** supported
- **High accuracy** transcription
- **Real-time processing**
- **Multiple audio formats** (WAV, OGG)
- **Configurable recognition models**
- **Automatic punctuation**
- **Enhanced models** for better accuracy

## 🚀 Quick Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your **Project ID** (you'll need this)

### Step 2: Enable Speech-to-Text API

1. In the Google Cloud Console, go to **APIs & Services** > **Library**
2. Search for "Speech-to-Text API"
3. Click **Enable**

### Step 3: Create Service Account

1. Go to **IAM & Admin** > **Service Accounts**
2. Click **Create Service Account**
3. Give it a name like "homeassistant-stt"
4. Click **Create and Continue**
5. Add role: **Speech-to-Text Service Agent**
6. Click **Continue** and **Done**

### Step 4: Generate Credentials

1. Click on your newly created service account
2. Go to **Keys** tab
3. Click **Add Key** > **Create new key**
4. Choose **JSON** format
5. Download the JSON file
6. **Keep this file secure!**

### Step 5: Configure Integration

1. In Home Assistant, go to **Settings** > **Integrations**
2. Find your **Gemini AI TTS/STT** integration
3. Click **Configure**
4. Enter your **Google Cloud Project ID**
5. Open the downloaded JSON file and copy **all the content**
6. Paste the JSON content into **Google Cloud Credentials JSON** field
7. Choose your preferred **STT Language** and **Model**
8. Save the configuration

## 🎛️ Configuration Options

### STT Languages

Choose from 60+ supported languages:

| Language | Code | Language | Code |
|----------|------|----------|------|
| English (US) | en-US | Spanish (Spain) | es-ES |
| English (UK) | en-GB | Spanish (US) | es-US |
| French (France) | fr-FR | German (Germany) | de-DE |
| Italian (Italy) | it-IT | Portuguese (Brazil) | pt-BR |
| Japanese (Japan) | ja-JP | Korean (Korea) | ko-KR |
| Chinese (Simplified) | zh-CN | Chinese (Traditional) | zh-TW |
| Arabic | ar | Hindi (India) | hi-IN |
| Russian (Russia) | ru-RU | Dutch (Netherlands) | nl-NL |

And many more...

### STT Models

| Model | Best For | Description |
|-------|----------|-------------|
| **latest_long** | Long audio files | Best for recordings longer than 1 minute |
| **latest_short** | Voice commands | Optimized for short commands and phrases |
| **command_and_search** | Voice control | Perfect for Home Assistant voice commands |
| **phone_call** | Phone audio | Optimized for telephone quality audio |
| **video** | Video content | Best for video/multimedia audio |
| **default** | General use | Good all-around performance |

## 🎯 Usage Examples

### Basic Voice Command

```yaml
# Voice automation example
automation:
  - alias: "Voice Control Lights"
    trigger:
      platform: conversation
      command: "turn on the living room lights"
    action:
      service: light.turn_on
      target:
        entity_id: light.living_room
```

### STT with Response

```yaml
# Process voice input and respond
automation:
  - alias: "Voice Question Response"
    trigger:
      platform: event
      event_type: voice_command_received
    action:
      - service: conversation.process
        data:
          text: "{{ trigger.event.data.text }}"
          agent_id: conversation.gemini_ai_conversation
        response_variable: ai_response
      - service: tts.speak
        data:
          entity_id: media_player.living_room
          message: "{{ ai_response.response.speech.plain.speech }}"
```

### Multi-language Support

```yaml
# Language-specific processing
automation:
  - alias: "Multi-language Voice Commands"
    trigger:
      platform: conversation
    condition:
      - condition: template
        value_template: "{{ trigger.text | length > 0 }}"
    action:
      - choose:
          - conditions:
              - condition: template
                value_template: "{{ 'hola' in trigger.text.lower() }}"
            sequence:
              - service: tts.speak
                data:
                  message: "¡Hola! ¿Cómo puedo ayudarte?"
                  options:
                    language: "es-US"
          - conditions:
              - condition: template
                value_template: "{{ 'bonjour' in trigger.text.lower() }}"
            sequence:
              - service: tts.speak
                data:
                  message: "Bonjour! Comment puis-je vous aider?"
                  options:
                    language: "fr-FR"
        default:
          - service: conversation.process
            data:
              text: "{{ trigger.text }}"
```

## 🔧 Advanced Configuration

### Optimize for Voice Commands

```yaml
# Best settings for Home Assistant voice commands
# In integration options:
# - STT Language: en-US (or your preferred language)
# - STT Model: command_and_search
# - Streaming: Enabled
```

### Optimize for Long Conversations

```yaml
# Best settings for extended conversations
# In integration options:
# - STT Language: en-US (or your preferred language)  
# - STT Model: latest_long
# - Streaming: Enabled
```

### Multi-language Household

```yaml
# Script to switch STT language dynamically
script:
  switch_stt_language:
    variables:
      languages:
        english: "en-US"
        spanish: "es-US"
        french: "fr-FR"
        german: "de-DE"
    sequence:
      - service: gemini_ai_tts.configure_stt
        data:
          language: "{{ languages[language_name] }}"
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "STT not configured" Warning

**Cause**: Missing Google Cloud credentials or project ID
**Solution**: 
- Verify project ID is correct
- Check JSON credentials are complete and valid
- Ensure Speech-to-Text API is enabled

#### 2. Poor Recognition Accuracy

**Cause**: Wrong model or language settings
**Solution**:
- Use `command_and_search` model for voice commands
- Use `latest_long` for longer audio
- Ensure correct language is selected
- Check audio quality and microphone

#### 3. "Authentication Error"

**Cause**: Invalid or expired credentials
**Solution**:
- Regenerate service account key
- Verify service account has Speech-to-Text permissions
- Check project billing is enabled

#### 4. "Quota Exceeded"

**Cause**: Google Cloud API quota limits
**Solution**:
- Check Google Cloud Console quotas
- Upgrade billing plan if needed
- Monitor usage patterns

### Performance Tips

1. **Use appropriate models**:
   - `command_and_search` for quick commands
   - `latest_long` for extended speech

2. **Optimize audio quality**:
   - Use good microphones
   - Minimize background noise
   - Ensure proper audio levels

3. **Language optimization**:
   - Set specific language codes (en-US vs en-GB)
   - Use region-appropriate languages

4. **Monitor usage**:
   - Check Google Cloud billing
   - Monitor API quotas
   - Track recognition accuracy

## 💰 Pricing

Google Cloud Speech-to-Text pricing (as of 2025):
- **Standard models**: $0.006 per 15 seconds
- **Enhanced models**: $0.009 per 15 seconds
- **Free tier**: 60 minutes per month

For typical Home Assistant usage (voice commands), costs are usually under $1-5 per month.

## 🔒 Security Best Practices

1. **Secure credentials storage**:
   - Never share service account JSON files
   - Use minimal required permissions
   - Rotate keys regularly

2. **Network security**:
   - Audio data is encrypted in transit
   - No audio stored by Google (configurable)
   - HTTPS connections only

3. **Privacy considerations**:
   - Audio processing occurs in Google Cloud
   - Review Google's privacy policies
   - Consider local STT alternatives for sensitive environments

## 🚀 Next Steps

With STT fully configured, you can:

1. **Set up voice commands** for device control
2. **Create conversational automations** with AI responses
3. **Build multi-language experiences** for international households
4. **Integrate with Home Assistant Assist** for comprehensive voice control
5. **Develop custom voice applications** using the conversation agent

Your smart home now has professional-grade speech recognition capabilities! 🎉
