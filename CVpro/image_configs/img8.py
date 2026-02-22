# ============================================================================
#                        IMAGE CONFIG — 8.jpg
# ============================================================================
# Edit ONLY this file when working on image 8 (8.jpg).
# Do NOT edit ui.py or colorextract.py for per-image customisation.
# ============================================================================

CONFIG = {
    # ── Extraction page: which color buttons to show ─────────────────────────
    'extract_colors': ['green', 'purple'],

    # ── Filter (Change Mood) page: which filter buttons to show ──────────────
    'filter_colors': ['red', 'blue', 'gray'],

    # ── Cinematic descriptions for each extraction color ─────────────────────
    'extract_descriptions': {
        'green': (
            "Cinematic Emotion",
            "Green extraction highlights the witch's green skin, the dark forest, grass, and the green sky. "
            "This makes the scene feel mysterious, magical, and slightly intense because the green tones "
            "emphasize the darker fantasy side of the image and the contrast between the witch and the environment.",
        ),
        'purple': (
            "Cinematic Emotion",
            "Pink extraction highlights the princess's dress, cherry blossoms, and soft pink flowers on the "
            "left side. This creates a warm, gentle, and dreamy mood, making the scene feel more elegant "
            "and romantic as the soft pink tones focus on beauty and softness.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinematic Emotion",
            "A red filter would make the scene feel more intense and dominant. It would add a "
            "sense of power, tension, and strong emotion, as if the moment is more dramatic.",
        ),
        'blue': (
            "Cinematic Emotion",
            "A blue filter would make the scene feel colder and more serious. It would reduce "
            "the warmth of the gold and create a calm but strict and formal atmosphere.",
        ),
        'gray': (
            "Cinematic Emotion",
            "A grayscale filter would make the scene look more historic and serious. It would "
            "remove the rich colors and focus more on the expression, costume, and royal details, "
            "giving a classic and dramatic tone.",
        ),
    },
}