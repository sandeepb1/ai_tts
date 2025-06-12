"""Constants for the Gemini AI TTS/STT integration."""
from __future__ import annotations

DOMAIN = "gemini_ai_tts"

# Configuration keys
CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_VOICE = "voice"
CONF_STYLE = "style"
CONF_EMOTION = "emotion"
CONF_PACE = "pace"
CONF_LANGUAGE = "language"
CONF_STREAMING = "streaming"
CONF_STT_PROJECT_ID = "stt_project_id"
CONF_STT_CREDENTIALS_JSON = "stt_credentials_json"
CONF_STT_LANGUAGE = "stt_language"
CONF_STT_MODEL = "stt_model"

# Default values
DEFAULT_MODEL_TTS = "gemini-2.5-flash-preview-tts"
DEFAULT_MODEL_CONVERSATION = "gemini-2.5-pro-preview-06-05"
DEFAULT_VOICE = "Puck"
DEFAULT_STYLE = "natural"
DEFAULT_LANGUAGE = "auto"
DEFAULT_STREAMING = True
DEFAULT_STT_LANGUAGE = "en-US"
DEFAULT_STT_MODEL = "latest_long"

# Available models - separated by category
CONVERSATION_MODELS = {
    "gemini-2.5-pro-preview-06-05": "Gemini 2.5 Pro (Conversation)",
    "gemini-2.0-flash": "Gemini 2.0 Flash (Fast Conversation)",
    "gemini-1.5-pro": "Gemini 1.5 Pro (Conversation)",
}

TTS_MODELS = {
    "gemini-2.5-flash-preview-tts": "Gemini 2.5 Flash TTS (Fast)",
    "gemini-2.5-pro-preview-tts": "Gemini 2.5 Pro TTS (High Quality)",
}

# Combined models for backward compatibility
MODELS = {**CONVERSATION_MODELS, **TTS_MODELS}

# Available voices with descriptions
VOICES = {
    "Zephyr": "Bright",
    "Puck": "Upbeat", 
    "Charon": "Informative",
    "Kore": "Firm",
    "Fenrir": "Excitable",
    "Leda": "Youthful",
    "Orus": "Firm",
    "Aoede": "Breezy",
    "Callirrhoe": "Easy-going",
    "Autonoe": "Bright",
    "Enceladus": "Breathy",
    "Iapetus": "Clear",
    "Umbriel": "Easy-going",
    "Algieba": "Smooth",
    "Despina": "Smooth",
    "Erinome": "Clear",
    "Algenib": "Gravelly",
    "Rasalgethi": "Informative",
    "Laomedeia": "Upbeat",
    "Achernar": "Soft",
    "Alnilam": "Firm",
    "Schedar": "Even",
    "Gacrux": "Mature",
    "Pulcherrima": "Forward",
    "Achird": "Friendly",
    "Zubenelgenubi": "Casual",
    "Vindemiatrix": "Gentle",
    "Sadachbia": "Lively",
    "Sadaltager": "Knowledgeable",
    "Sulafat": "Warm"
}

# Speech styles
SPEECH_STYLES = [
    "natural",
    "cheerful", 
    "excited",
    "calm",
    "professional",
    "friendly",
    "mysterious",
    "dramatic",
    "whisper",
    "confident"
]

# Emotions
EMOTIONS = [
    "neutral",
    "happy",
    "sad", 
    "angry",
    "surprised",
    "disgusted",
    "fearful",
    "excited",
    "calm",
    "serious"
]

# Pace options
PACE_OPTIONS = [
    "very_slow",
    "slow", 
    "normal",
    "fast",
    "very_fast"
]

# Supported languages
SUPPORTED_LANGUAGES = {
    "ar-EG": "Arabic (Egyptian)",
    "en-US": "English (US)",
    "es-US": "Spanish (US)", 
    "fr-FR": "French (France)",
    "de-DE": "German (Germany)",
    "hi-IN": "Hindi (India)",
    "id-ID": "Indonesian (Indonesia)",
    "it-IT": "Italian (Italy)",
    "ja-JP": "Japanese (Japan)",
    "ko-KR": "Korean (Korea)",
    "pt-BR": "Portuguese (Brazil)",
    "ru-RU": "Russian (Russia)",
    "nl-NL": "Dutch (Netherlands)",
    "pl-PL": "Polish (Poland)",
    "th-TH": "Thai (Thailand)",
    "tr-TR": "Turkish (Turkey)",
    "vi-VN": "Vietnamese (Vietnam)",
    "ro-RO": "Romanian (Romania)",
    "uk-UA": "Ukrainian (Ukraine)",
    "bn-BD": "Bengali (Bangladesh)",
    "en-IN": "English (India)",
    "mr-IN": "Marathi (India)",
    "ta-IN": "Tamil (India)",
    "te-IN": "Telugu (India)",
    "auto": "Auto-detect"
}

# STT languages (Google Cloud Speech-to-Text supported)
STT_SUPPORTED_LANGUAGES = {
    "en-US": "English (US)",
    "en-GB": "English (UK)",
    "en-AU": "English (Australia)",
    "en-CA": "English (Canada)",
    "en-IN": "English (India)",
    "es-ES": "Spanish (Spain)",
    "es-US": "Spanish (US)",
    "fr-FR": "French (France)",
    "fr-CA": "French (Canada)",
    "de-DE": "German (Germany)",
    "it-IT": "Italian (Italy)",
    "pt-BR": "Portuguese (Brazil)",
    "pt-PT": "Portuguese (Portugal)",
    "ru-RU": "Russian (Russia)",
    "ja-JP": "Japanese (Japan)",
    "ko-KR": "Korean (Korea)",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ar": "Arabic",
    "hi-IN": "Hindi (India)",
    "th-TH": "Thai (Thailand)",
    "tr-TR": "Turkish (Turkey)",
    "nl-NL": "Dutch (Netherlands)",
    "pl-PL": "Polish (Poland)",
    "sv-SE": "Swedish (Sweden)",
    "da-DK": "Danish (Denmark)",
    "no-NO": "Norwegian (Norway)",
    "fi-FI": "Finnish (Finland)",
    "uk-UA": "Ukrainian (Ukraine)",
    "cs-CZ": "Czech (Czech Republic)",
    "sk-SK": "Slovak (Slovakia)",
    "hu-HU": "Hungarian (Hungary)",
    "ro-RO": "Romanian (Romania)",
    "bg-BG": "Bulgarian (Bulgaria)",
    "hr-HR": "Croatian (Croatia)",
    "sl-SI": "Slovenian (Slovenia)",
    "et-EE": "Estonian (Estonia)",
    "lv-LV": "Latvian (Latvia)",
    "lt-LT": "Lithuanian (Lithuania)",
    "mt-MT": "Maltese (Malta)",
    "ga-IE": "Irish (Ireland)",
    "cy-GB": "Welsh (UK)",
    "eu-ES": "Basque (Spain)",
    "ca-ES": "Catalan (Spain)",
    "gl-ES": "Galician (Spain)",
    "is-IS": "Icelandic (Iceland)",
    "mk-MK": "Macedonian (North Macedonia)",
    "sq-AL": "Albanian (Albania)",
    "sr-RS": "Serbian (Serbia)",
    "bs-BA": "Bosnian (Bosnia and Herzegovina)",
    "mn-MN": "Mongolian (Mongolia)",
    "ne-NP": "Nepali (Nepal)",
    "si-LK": "Sinhala (Sri Lanka)",
    "ta-IN": "Tamil (India)",
    "te-IN": "Telugu (India)",
    "ml-IN": "Malayalam (India)",
    "kn-IN": "Kannada (India)",
    "gu-IN": "Gujarati (India)",
    "bn-IN": "Bengali (India)",
    "pa-IN": "Punjabi (India)",
    "mr-IN": "Marathi (India)",
    "or-IN": "Odia (India)",
    "as-IN": "Assamese (India)",
    "ur-PK": "Urdu (Pakistan)",
    "fa-IR": "Persian (Iran)",
    "he-IL": "Hebrew (Israel)",
    "vi-VN": "Vietnamese (Vietnam)",
    "id-ID": "Indonesian (Indonesia)",
    "ms-MY": "Malay (Malaysia)",
    "fil-PH": "Filipino (Philippines)",
    "km-KH": "Khmer (Cambodia)",
    "lo-LA": "Lao (Laos)",
    "my-MM": "Myanmar (Burma)",
    "ka-GE": "Georgian (Georgia)",
    "am-ET": "Amharic (Ethiopia)",
    "sw-KE": "Swahili (Kenya)",
    "zu-ZA": "Zulu (South Africa)",
    "af-ZA": "Afrikaans (South Africa)",
}

# STT model options
STT_MODELS = {
    "latest_long": "Latest Long (Best for long audio)",
    "latest_short": "Latest Short (Best for short commands)",
    "command_and_search": "Command and Search (Optimized for voice commands)",
    "phone_call": "Phone Call (Optimized for phone audio)",
    "video": "Video (Optimized for video audio)",
    "default": "Default (General purpose)",
}

# Audio settings
AUDIO_SAMPLE_RATE = 24000
AUDIO_CHANNELS = 1
AUDIO_SAMPLE_WIDTH = 2
AUDIO_FORMAT = "wav"

# API settings
API_TIMEOUT = 30
MAX_TEXT_LENGTH = 8000
CONTEXT_WINDOW = 32000
