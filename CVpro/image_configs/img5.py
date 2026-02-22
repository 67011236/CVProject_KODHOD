# ============================================================================
#                        IMAGE CONFIG — 5.jpg
# ============================================================================
# Edit ONLY this file when working on image 5 (5.jpg).
# Do NOT edit ui.py or colorextract.py for per-image customisation.
# ============================================================================

CONFIG = {
    # ── Extraction page: which color buttons to show ─────────────────────────
    'extract_colors': ['black', 'red'],

    # ── Filter (Change Mood) page: which filter buttons to show ──────────────
    'filter_colors': ['red', 'blue', 'yellow'],

    # ── Cinematic descriptions for each extraction color ─────────────────────
    'extract_descriptions': {
        'black': (
            "Cinematic Emotion",
            "The dark blue and black tones create a heavy, mysterious, and ominous mood. These dark "
            "colors make the scene feel serious, dangerous, and secretive, as if something powerful "
            "and forbidden is happening. It gives a sense of fear and tension, especially with the "
            "large skull and dim environment.",
        ),
        'red': (
            "Cinematic Emotion",
            "The orange candle light adds a warm but eerie feeling to the scene. Instead of feeling "
            "safe, the warm glow makes the place look ritualistic and intense, as if it is part of "
            "a ceremony. This color highlights the main object and characters, making the moment "
            "feel dramatic and important.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinematic Emotion",
            "The red color would make the scene feel more intense, dangerous, and dramatic. It would "
            "increase the sense of fear and tension, making the ritual-like setting look more "
            "aggressive and threatening, as if something powerful or violent is about to happen.",
        ),
        'blue': (
            "Cinematic Emotion",
            "The blue color would make the scene feel colder, darker, and more mysterious. It would "
            "reduce warmth from the candles and create a calm but eerie mood, making the place seem "
            "more secretive and supernatural.",
        ),
        'yellow': (
            "Cinematic Emotion",
            "The yellow color would make the scene brighter but still tense. It would highlight the "
            "candles and main object more, giving the scene a ritual and focused feeling, as if an "
            "important ceremony is taking place while still keeping a serious and suspenseful tone.",
        ),
    },
}