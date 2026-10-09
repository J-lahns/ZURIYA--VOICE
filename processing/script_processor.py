# ==========================================
# ZURIYA VOICE ENGINE
# Script Processor v1.8
# ==========================================

import re


# ==========================================
# PAUSE SETTINGS
# ==========================================

PAUSE_DURATION = 0.15

LONG_PAUSE_DURATION = 0.40


# ==========================================
# SCRIPT PROCESSOR
# ==========================================

def process_script(text):
    """
    Process ZURIYA script markers.

    Supported markers:

    [PAUSE]
    [LONG_PAUSE]

    Returns:
        ordered segments
    """

    segments = []


    # ======================================
    # FIND TEXT AND PAUSE MARKERS
    # ======================================

    pattern = r"\[(PAUSE|LONG_PAUSE)\]"

    parts = re.split(
        pattern,
        text
    )


    # ======================================
    # PROCESS SEGMENTS
    # ======================================

    for i, part in enumerate(parts):

        part = part.strip()

        # ----------------------------------
        # NORMAL TEXT
        # ----------------------------------

        if i % 2 == 0:

            if part:

                segments.append({
                    "type": "text",
                    "content": part
                })


        # ----------------------------------
        # PAUSE MARKERS
        # ----------------------------------

        else:

            if part == "PAUSE":

                segments.append({
                    "type": "pause",
                    "duration": PAUSE_DURATION
                })

            elif part == "LONG_PAUSE":

                segments.append({
                    "type": "pause",
                    "duration": LONG_PAUSE_DURATION
                })


    return segments