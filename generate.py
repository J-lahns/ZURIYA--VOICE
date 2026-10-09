from kokoro import KPipeline
import soundfile as sf
import numpy as np
from pathlib import Path
import sys
import json

from processing.script_processor import process_script

from config import (
    ACTIVE_PROFILE,
    VOICE_PROFILES,
    LANGUAGE,
    SAMPLE_RATE,
    CHUNK_PAUSE,
    TARGET_PEAK
)

# ==========================================
# ZURIYA VOICE ENGINE v1.8
# ==========================================


# ==========================================
# FOLDERS
# ==========================================

BASE_DIR = Path(__file__).parent

SCRIPT_DIR = BASE_DIR / "scripts"
EPISODE_DIR = BASE_DIR / "episodes"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================
# TERMINAL HELPERS
# ==========================================

def error(message):

    print()
    print("ERROR:", message)
    print()

    sys.exit(1)


def success(message):

    print()
    print(message)


# ==========================================
# EPISODE SELECTION
# ==========================================

if len(sys.argv) > 1:

    episode = sys.argv[1].strip()

else:

    episode = "episode_001"


# Remove .txt if provided

if episode.endswith(".txt"):

    episode = Path(episode).stem


# Validate episode name

if "/" in episode or "\\" in episode:

    error(
        "Invalid episode name. "
        "Use something like episode_001."
    )


if not episode:

    error("Episode name cannot be empty.")
# ==========================================
# EPISODE CONFIGURATION
# ==========================================

episode_config_file = (
    EPISODE_DIR / f"{episode}.json"
)

if not episode_config_file.exists():

    error(
        f"Episode configuration not found.\n"
        f"Expected:\n"
        f"  {episode_config_file}"
    )
print("Loading episode configuration...")

try:

    episode_config = json.loads(
        episode_config_file.read_text(
            encoding="utf-8"
        )
    )

except json.JSONDecodeError as e:

    error(
        f"Invalid episode configuration.\n"
        f"{e}"
    )

except Exception as e:

    error(
        f"Could not read episode configuration.\n"
        f"{e}"
    )
# ==========================================
# EPISODE SETTINGS
# ==========================================

EPISODE_TITLE = episode_config.get(
    "title",
    episode
)

EPISODE_PROFILE = episode_config.get(
    "voice_profile",
    ACTIVE_PROFILE
)

EPISODE_CHUNK_PAUSE = episode_config.get(
    "chunk_pause",
    CHUNK_PAUSE
)

EPISODE_TARGET_PEAK = episode_config.get(
    "target_peak",
    TARGET_PEAK
)
# ==========================================
# ACTIVE VOICE PROFILE
# ==========================================

if EPISODE_PROFILE not in VOICE_PROFILES:

    print()
    print(
        f"ERROR: Voice profile "
        f"'{EPISODE_PROFILE}' not found."
    )
    print()

    print("Available profiles:")

    for profile in VOICE_PROFILES:

        print(f"  - {profile}")

    print()

    sys.exit(1)


profile = VOICE_PROFILES[EPISODE_PROFILE]

VOICE = profile["voice"]

SPEED = profile["speed"]

PROFILE_DESCRIPTION = profile["description"]

# ==========================================
# FILE PATHS
# ==========================================

script_file = SCRIPT_DIR / f"{episode}.txt"

output_file = OUTPUT_DIR / f"{episode}.wav"


# ==========================================
# SCRIPT VALIDATION
# ==========================================

if not script_file.exists():

    print()
    print("ERROR: Script not found.")
    print()
    print(f"Expected:")
    print(f"  {script_file}")
    print()

    print("Available scripts:")

    scripts = sorted(
        SCRIPT_DIR.glob("*.txt")
    )

    if scripts:

        for script in scripts:

            print(
                f"  - {script.stem}"
            )

    else:

        print("  No scripts found.")

    print()

    sys.exit(1)


# ==========================================
# READ SCRIPT
# ==========================================
text = script_file.read_text(
    encoding="utf-8"
).strip()


if not text:

    error(
        f"The script '{script_file.name}' "
        "is empty."
    )


# ==========================================
# SCRIPT PROCESSING
# ==========================================

print("Processing script...")

try:

    segments = process_script(
        text
    )

except Exception as e:

    error(
        f"Script processing failed.\n"
        f"{e}"
    )


text_segments = sum(
    1
    for segment in segments
    if segment["type"] == "text"
)

pause_segments = sum(
    1
    for segment in segments
    if segment["type"] == "pause"
)


print(
    f"Text segments:  {text_segments}"
)

print(
    f"Pause segments: {pause_segments}"
)
# ==========================================
# OUTPUT PROTECTION
# ==========================================

if output_file.exists():

    print()
    print(
        f"Output already exists:"
    )

    print(
        f"  {output_file}"
    )

    print()

    choice = input(
        "Overwrite this file? [y/N]: "
    ).strip().lower()

    if choice != "y":

        print()
        print(
            "Generation cancelled."
        )
        print()

        sys.exit(0)


# ==========================================
# ENGINE HEADER
# ==========================================

print()
print("===================================")
print("      ZURIYA VOICE ENGINE v1.8")
print("===================================")
print()

print(f"Episode:       {episode}")
print(f"Title:         {EPISODE_TITLE}")
print(f"Profile:       {EPISODE_PROFILE}")
print(f"Voice:         {VOICE}")
print(f"Speed:         {SPEED}")
print(f"Sample Rate:   {SAMPLE_RATE}")
print(f"Chunk Pause:   {EPISODE_CHUNK_PAUSE}s")
print(f"Target Peak:   {EPISODE_TARGET_PEAK}")
print()

print(
    f"Script:        {script_file.name}"
)

print(
    f"Output:        {output_file.name}"
)

print()


# ==========================================
# INITIALIZE KOKORO
# ==========================================

print("Initializing Kokoro...")

try:

    pipeline = KPipeline(
        lang_code=LANGUAGE
    )

except Exception as e:

    error(
        f"Could not initialize Kokoro.\n"
        f"{e}"
    )


# ==========================================
# GENERATE NARRATION
# ==========================================

print("Generating narration...")

audio_parts = []

part_counter = 0


for segment in segments:

    # ======================================
    # TEXT SEGMENT
    # ======================================

    if segment["type"] == "text":

        segment_text = segment["content"]

        print()
        print("Generating text segment...")
        print(f"  {segment_text}")

        generator = pipeline(
            segment_text,
            voice=VOICE,
            speed=SPEED
        )

        segment_audio_parts = []


        for _, _, audio in generator:

            print(
                f"Generated part "
                f"{part_counter:02d}"
            )

            segment_audio_parts.append(
                audio
            )

            part_counter += 1


        

        # ----------------------------------
        # Combine Kokoro chunks
        # ----------------------------------

        if segment_audio_parts:

            for i, audio in enumerate(
                segment_audio_parts
            ):

                audio_parts.append(audio)

                if i < len(segment_audio_parts) - 1:

                    pause_samples = int(
                        EPISODE_CHUNK_PAUSE * SAMPLE_RATE
                    )

                    chunk_silence = np.zeros(
                        pause_samples,
                        dtype=np.float32
                    )

                    audio_parts.append(
                        chunk_silence
                    )


    # ======================================
    # PAUSE SEGMENT
    # ======================================

    elif segment["type"] == "pause":

        duration = segment["duration"]

        print()
        print(
            f"Adding pause: "
            f"{duration:.2f} seconds"
        )

        pause_samples = int(
            duration * SAMPLE_RATE
        )

        silence = np.zeros(
            pause_samples,
            dtype=np.float32
        )

        audio_parts.append(
            silence
        )

# ==========================================
# CHECK GENERATED AUDIO
# ==========================================

if not audio_parts:

    error(
        "Kokoro generated no audio."
    )




# ==========================================
# MERGE AUDIO
# ==========================================

print()
print("Combining narration...")

if not audio_parts:

    error(
        "No audio was generated. "
        "Please check the episode script."
    )

final_audio = np.concatenate(
    audio_parts
)


# ==========================================
# AUDIO NORMALIZATION
# ==========================================

print("Normalizing audio...")

peak = np.max(
    np.abs(final_audio)
)

if peak > 0:

    final_audio = (
        final_audio / peak
    ) * EPISODE_TARGET_PEAK
# ==========================================
# SAVE AUDIO
# ==========================================

print("Saving master narration...")

try:

    sf.write(
        output_file,
        final_audio,
        SAMPLE_RATE
    )

except Exception as e:

    error(
        f"Could not save audio.\n"
        f"{e}"
    )


# ==========================================
# AUDIO INFORMATION
# ==========================================

duration = (
    len(final_audio)
    / SAMPLE_RATE
)

minutes = int(
    duration // 60
)

seconds = duration % 60


# ==========================================
# COMPLETE
# ==========================================

print()
print("===================================")
print("       GENERATION COMPLETE")
print("===================================")
print()

print(f"Episode:   {episode}")
print(
    f"Duration:  "
    f"{minutes}m {seconds:.2f}s"
)

print(
    f"Output:    {output_file}"
)

print()

success(
    "ZURIYA narration is ready."
)

print()