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
    'filter_colors': ['red', 'yellow', 'gray'],

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
            "The red filter intensifies the ritualistic atmosphere, making the warm candle glow "
            "appear more dramatic and ceremonial. It enhances the sense of forbidden ritual and "
            "adds intensity to the mysterious gathering around the skull.",
        ),
        'yellow': (
            "Cinematic Emotion",
            "The yellow filter brightens the scene with golden warmth, transforming the eerie "
            "candlelight into a more prominent feature. It creates a focus on the central elements "
            "while maintaining the mysterious and ceremonial mood of the gathering.",
        ),
        'gray': (
            "Cinematic Emotion",
            "The grayscale filter removes all warmth and color, creating a cold, stark atmosphere "
            "that emphasizes the ominous nature of the scene. It makes the ritual appear more "
            "serious and foreboding, focusing purely on the dramatic composition.",
        ),
    },
}