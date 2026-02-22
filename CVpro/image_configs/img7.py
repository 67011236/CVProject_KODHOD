# ============================================================================
#                        IMAGE CONFIG — 7.jpg
# ============================================================================
# Edit ONLY this file when working on image 7 (7.jpg).
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
            "The black color creates a dark, powerful, and intimidating mood. It makes the character look "
            "strong, mysterious, and slightly dangerous. This color adds a serious and dramatic feeling to "
            "the scene.",
        ),
        'red': (
            "Cinematic Emotion",
            "The red color adds intensity and aggression to the image. It creates a sense of danger, power, "
            "and tension, especially with the red sky in the background. This makes the scene feel dramatic "
            "and bold.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinematic Emotion",
            "When the red filter is applied, the image shifts from a balanced and natural mood to a more "
            "intense and dramatic feeling. The atmosphere becomes hotter and more aggressive. It feels more "
            "powerful and action-focused compared to the original version.",
        ),
        'yellow': (
            "Cinematic Emotion",
            "When the yellow filter is added, the mood changes from natural and cool to warm and energetic. "
            "The image feels brighter and more vibrant. It gives a sunny, dynamic feeling instead of the "
            "calm tone in the original.",
        ),
        'gray': (
            "Cinematic Emotion",
            "When the grayscale filter is used, the image changes from colorful and lively to serious and "
            "emotional. The removal of color creates a more dramatic and cinematic mood. It feels calmer "
            "but also more intense in a subtle way.",
        ),
    },
}
