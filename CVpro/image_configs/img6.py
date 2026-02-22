# ============================================================================
#                        IMAGE CONFIG — 6.jpg
# ============================================================================
# Edit ONLY this file when working on image 6 (6.jpg).
# Do NOT edit ui.py or colorextract.py for per-image customisation.
# ============================================================================

CONFIG = {
    # ── Extraction page: which color buttons to show ─────────────────────────
    'extract_colors': ['purple', 'blue'],

    # ── Filter (Change Mood) page: which filter buttons to show ──────────────
    'filter_colors': ['red', 'purple', 'gray'],

    # ── Cinematic descriptions for each extraction color ─────────────────────
    'extract_descriptions': {
        'purple': (
            "Cinematic Emotion",
            "The pink color brings a playful and expressive mood. It shifts the feeling from calm or serious "
            "to more emotional and animated. Pink adds warmth and personality, making the scene feel more "
            "lively and dynamic.",
        ),
        'blue': (
            "Cinematic Emotion",
            "When focusing on the blue tone, the mood feels calm but also serious and thoughtful. Blue gives "
            "a sense of sadness, intelligence, and emotional depth. It shifts the atmosphere from energetic "
            "to more reflective and sensitive.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinematic Emotion",
            "A red filter would make the scene feel more intense and dramatic. The emotions would seem stronger, "
            "and the moment would feel more urgent or stressful.",
        ),
        'purple': (
            "Cinematic Emotion",
            "A purple filter would give the scene a more magical and mysterious mood. It would make the environment "
            "feel imaginative and emotional, like a deep internal moment.",
        ),
        'gray': (
            "Cinematic Emotion",
            "A grayscale filter would remove the bright emotions and make the scene feel more serious and quiet. "
            "It would shift the mood to something more reflective and less energetic.",
        ),
    },
}
