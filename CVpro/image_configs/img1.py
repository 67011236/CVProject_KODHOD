# ============================================================================
#                        IMAGE CONFIG — 1.jpg
# ============================================================================
# Edit ONLY this file when working on image 1 (1.jpg).
# Do NOT edit ui.py or colorextract.py for per-image customisation.
# ============================================================================

CONFIG = {
    # ── Extraction page: which color buttons to show ─────────────────────────
    'extract_colors': ['green', 'purple'],

    # ── Filter (Change Mood) page: which filter buttons to show ──────────────
    'filter_colors': ['red', 'yellow', 'gray'],

    # ── Cinematic descriptions for each extraction color ─────────────────────
    'extract_descriptions': {
        'green': (
            "Cinematic Emotion",
            "This unnatural green shade represents the character's detachment from society. "
            "It creates a sense of unease and isolation, highlighting a world where the individual "
            "feels like an outsider in their own environment.",
        ),
        'purple': (
            "Cinematic Emotion",
            "A somber, low-luminance tone that evokes a feeling of nostalgia and loneliness. "
            "When paired with green, it creates visual tension that reflects the quiet sadness "
            "and solitude of life in a vast, empty city.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinematic Emotion",
            "The intense red implies a character boiling with inner frustration or anger, "
            "hiding behind a calm face while trapped in a confined space.",
        ),
        'yellow': (
            "Cinematic Emotion",
            "The golden glow suggests a moment of pure euphoria or spiritual awakening, "
            "where the character is experiencing an internal joy that detaches them from reality.",
        ),
        'gray': (
            "Cinematic Emotion",
            "Beyond just sadness, the gray represents loss of identity. The character isn't resting; "
            "they are becoming a ghost in a world that has lost all meaning.",
        ),
    },
}
