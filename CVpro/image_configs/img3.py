# ============================================================================
#                        IMAGE CONFIG — 3.jpg
# ============================================================================
# Edit ONLY this file when working on image 3 (3.jpg).
# Do NOT edit ui.py or colorextract.py for per-image customisation.
# ============================================================================

CONFIG = {
    # ── Extraction page: which color buttons to show ─────────────────────────
    'extract_colors': ['green', 'black'],

    # ── Filter (Change Mood) page: which filter buttons to show ──────────────
    'filter_colors': ['red', 'blue', 'gray'],

    # ── Cinematic descriptions for each extraction color ─────────────────────
    'extract_descriptions': {
        'green': (
            "Cinematic Emotion",
            "This vibrant Acid Green evokes a sense of supernatural power and eerie intensity. "
            "It transforms characters into monstrous entities, signaling high-energy danger "
            "and unpredictability within a dark setting.",
        ),
        'black': (
            "Cinematic Emotion",
            "The deep black void represents the unknown and absolute isolation. "
            "By stripping away all environmental context, it creates a high-pressure visual focus "
            "that makes the glowing subjects appear more imposing and predatory.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinematic Emotion",
            "The red filter transforms the glowing smoke into blazing fire. It shifts the scene from a "
            "spooky cartoon to an immediate, aggressive threat, making the characters look like "
            "dangerous entities emerging from hellfire.",
        ),
        'blue': (
            "Cinematic Emotion",
            "The blue filter casts a freezing chill over the scene. The glowing energy turns into a "
            "cold, ghostly light (like moonlight), making the characters appear as sorrowful spirits "
            "wandering in the deep night, rather than active threats.",
        ),
        'gray': (
            "Cinematic Emotion",
            "Stripping away the color turns the smoke into chilling, ash-like fog. It removes the "
            "energetic vibe, leaving a bleak, lifeless atmosphere reminiscent of a classic gothic "
            "horror or a hopeless nightmare.",
        ),
    },
}
