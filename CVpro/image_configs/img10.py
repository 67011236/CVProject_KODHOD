# ============================================================================
#                        IMAGE CONFIG — 10.jpg
# ============================================================================
# Edit ONLY this file when working on image 10 (10.jpg).
# Do NOT edit ui.py or colorextract.py for per-image customisation.
# ============================================================================

CONFIG = {
    # ── Extraction page: which color buttons to show ─────────────────────────
    'extract_colors': ['yellow', 'black'],

    # ── Filter (Change Mood) page: which filter buttons to show ──────────────
    'filter_colors': ['red', 'blue', 'gray'],

    # ── Cinematic descriptions for each extraction color ─────────────────────
    'extract_descriptions': {
        'yellow': (
            "Cinematic Emotion",
            "The golden-orange tones enveloping the entire frame signify Hope and warmth amidst the "
            "harshness of the desert. It represents a fleeting moment of deep emotional connection "
            "between the characters in a world fraught with danger.",
        ),
        'black': (
            "Cinematic Emotion",
            "The deep brown shades and overlapping shadows symbolize a heavy Destiny and the profound "
            "mystery of the Arrakis desert, which stands ready to consume everything in its path.",
        ),
    },

    # ── Cinematic descriptions for each filter ────────────────────────────────
    'filter_descriptions': {
        'red': (
            "Cinnamon Dusk - Power & Bloodshed",
            "A deeper, reddish-brown tone that hints at the \"Spice\" and the looming violence of war, "
            "creating a tense atmosphere of impending doom.",
        ),
        'blue': (
            "Twilight Blue - Melancholy & Calm",
            "By cooling down the warmth of the sand, this tone introduces a sense of stillness and "
            "sadness, highlighting the rare moments of peace before the inevitable conflict.",
        ),
        'gray': (
            "Cinematic Emotion",
            "A grayscale filter would make the scene look more historic and serious. It would "
            "remove the rich colors and focus more on the expression, costume, and royal details, "
            "giving a classic and dramatic tone.",
        ),
    },
}