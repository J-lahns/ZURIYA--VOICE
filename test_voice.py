from kokoro import KPipeline
import soundfile as sf

pipeline = KPipeline(lang_code="a")

text = """
Before history remembered them,
there was a story.

Around ancient fires, elders spoke of kings,
warriors, spirits, and forgotten kingdoms.

Some stories were written down.

Others disappeared with the voices that carried them.

But every once in a while,
the past leaves a clue.

A ruin.
A name.
A forgotten road.

And when we follow it,
we discover something remarkable.

The story was never truly lost.
"""

generator = pipeline(
    text,
    voice="am_michael",
    speed=1.0
)

for i, (_, _, audio) in enumerate(generator):
    filename = f"zuriya_test_{i}.wav"
    sf.write(filename, audio, 24000)
    print(f"Created: {filename}")