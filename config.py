# ==========================================
# ZURIYA VOICE ENGINE
# Configuration
# ==========================================


# ==========================================
# ACTIVE VOICE PROFILE
# ==========================================

ACTIVE_PROFILE = "keeper"


# ==========================================
# VOICE PROFILES
# ==========================================

VOICE_PROFILES = {

    "keeper": {
        "voice": "am_michael",
        "speed": 1.0,
        "description": "THE KEEPER - primary ZURIYA narrator"
    },

    "keeper_slow": {
        "voice": "am_michael",
        "speed": 0.92,
        "description": "THE KEEPER - slower cinematic delivery"
    },

    "keeper_fast": {
        "voice": "am_michael",
        "speed": 1.08,
        "description": "THE KEEPER - faster energetic delivery"
    }

}


# ==========================================
# AUDIO SETTINGS
# ==========================================

LANGUAGE = "a"

SAMPLE_RATE = 24000

CHUNK_PAUSE = 0.15

TARGET_PEAK = 0.95