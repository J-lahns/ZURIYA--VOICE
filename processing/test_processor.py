# ==========================================
# ZURIYA VOICE ENGINE
# Script Processor Test v1.8
# ==========================================

from script_processor import process_script


# ==========================================
# TEST SCRIPT
# ==========================================

test_script = """
Before history remembered them...

[PAUSE]

There was a story.

[LONG_PAUSE]

A story that refused to die.
"""


# ==========================================
# PROCESS SCRIPT
# ==========================================

segments = process_script(
    test_script
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print()
print("===================================")
print("   ZURIYA SCRIPT PROCESSOR v1.8")
print("===================================")
print()

print("ORIGINAL SCRIPT:")
print("-----------------------------------")
print(test_script)

print()
print("PROCESSED SEGMENTS:")
print("-----------------------------------")


for i, segment in enumerate(segments):

    if segment["type"] == "text":

        print(
            f"Segment {i + 1}: TEXT"
        )

        print(
            f"  {segment['content']}"
        )

    elif segment["type"] == "pause":

        print(
            f"Segment {i + 1}: PAUSE"
        )

        print(
            f"  Duration: "
            f"{segment['duration']:.2f} seconds"
        )

    print()


print("===================================")
print("          TEST COMPLETE")
print("===================================")