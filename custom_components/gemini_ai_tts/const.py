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
CONF_MULTI_SPEAKER = "multi_speaker"

# Default values
DEFAULT_MODEL_TTS = "gemini-2.5-flash-preview-tts"
DEFAULT_MODEL_CONVERSATION = "gemini-2.5-pro-preview-06-05"
DEFAULT_VOICE = "Puck"
DEFAULT_STYLE = "natural"
DEFAULT_LANGUAGE = "auto"
DEFAULT_STREAMING = True

# Available models
MODELS = {
    "gemini-2.5-flash-preview-tts": "Gemini 2.5 Flash TTS (Fast)",
    "gemini-2.5-pro-preview-tts": "Gemini 2.5 Pro TTS (High Quality)",
    "gemini-2.5-pro-preview-06-05": "Gemini 2.5 Pro (Conversation)",
}

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

# Audio settings
AUDIO_SAMPLE_RATE = 24000
AUDIO_CHANNELS = 1
AUDIO_SAMPLE_WIDTH = 2
AUDIO_FORMAT = "wav"

# API settings
API_TIMEOUT = 30
MAX_TEXT_LENGTH = 8000
CONTEXT_WINDOW = 32000
