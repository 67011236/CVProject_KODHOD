# ============================================================================
#                        IMAGE CONFIG — 4.jpg
# ============================================================================
# Edit ONLY this file when working on image 4 (4.jpg).
# Do NOT edit ui.py or colorextract.py for per-image customisation.
# ============================================================================

CONFIG = {
    # ── Extraction page: which color buttons to show ─────────────────────────
    'extract_colors': ['blue', 'yellow'],

    # ── Filter (Change Mood) page: which filter buttons to show ──────────────
    'filter_colors': ['red', 'yellow', 'gray'],

    # ── Cinematic descriptions for each extraction color ─────────────────────
    'extract_descriptions': {
        'blue': (
            "Cinematic Emotion",
            "The blue color creates a dark and mysterious mood. It feels calm but also secretive, "
            "like something hidden is happening at night. This makes the scene look suspicious and "
            "suggests the characters might be planning something sneaky or not good.",
        ),
        'yellow': (
            "Cinematic Emotion",
            "The yellow color adds a warm light that focuses attention on the characters inside the room. "
            "It suggests activity and thinking, as if they are discussing or planning something. The warm "
            "yellow against the dark background makes the scene feel tense and intentional, hinting at a hidden plan.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinematic Emotion",
            "The red color changes the scene into a more intense and tense mood. It feels dramatic, "
            "emotional, and slightly dangerous. This makes the characters seem more serious, as if "
            "they are arguing or planning something risky.",
        ),
        'yellow': (
            "Cinematic Emotion",
            "The yellow color gives the scene a warmer and more active feeling. It looks brighter and "
            "more focused on the characters, suggesting they are thinking or discussing a plan. The mood "
            "feels tense but more alert than scary.",
        ),
        'gray': (
            "Cinematic Emotion",
            "The grayscale color removes warmth and makes the scene feel serious and quiet. It creates "
            "a cold and dramatic mood, as if the moment is important or secret. This makes the scene "
            "feel more suspicious and thoughtful.",
        ),
    },
}