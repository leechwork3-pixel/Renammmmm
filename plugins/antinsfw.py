from pyrogram.types import Message
import re

# ─────────────────────────────────────────────
# NSFW keyword categories
# ─────────────────────────────────────────────
nsfw_keywords = {
    "general": [
        "porn", "sex", "nude", "naked", "boobs", "tits", "pussy", "dick", "cock", "ass",
        "fuck", "blowjob", "cum", "orgasm", "shemale", "erotic", "masturbate", "anal",
        "hardcore", "bdsm", "fetish", "lingerie", "xxx", "milf", "gay", "lesbian",
        "threesome", "squirting", "butt plug", "dildo", "vibrator", "escort", "handjob",
        "striptease", "kinky", "pornstar", "sex tape", "spank", "swinger", "taboo", "cumshot",
        "deepthroat", "domination", "submission", "handcuffs", "orgy", "roleplay", "sex toy",
        "voyeur", "cosplay", "adult", "culture", "pornhwa", "netorare", "netori", "netorase",
        "eromanga", "incest", "stepmom", "stepdad", "stepsister", "stepbrother", "stepson",
        "stepdaughter", "ntr", "gangbang", "facial", "golden shower", "pegging", "rimming",
        "rough sex", "dirty talk", "sex chat", "nude pic", "lewd", "titty", "twerk", "breasts",
        "penis", "vagina", "clitoris", "genitals", "sexual", "kamasutra", "pedo", "rape",
        "bondage", "cum inside", "creampie", "sex slave", "sex doll", "sex machine", "latex",
        "oral sex", "slut", "whore", "tramp", "skank", "cumdumpster", "cultured",
        "ecchi", "doujin", "hentai", "smut", "waifu", "futanari", "tentacle"
    ],
    "hentai": [
        "hentai", "doujinshi", "ecchi", "yaoi", "shota", "loli", "tentacle", "futanari",
        "bishoujo", "bishounen", "mecha hentai", "hentai manga", "hentai anime", "smut",
        "eroge", "visual novel", "h-manga", "h-anime", "adult manga", "18+ anime", "18+ manga",
        "lewd anime", "lewd manga", "animated porn", "animated sex", "hentai game", "hentai art",
        "hentai drawing", "hentai doujin", "yaoi hentai", "hentai comic", "hentai picture",
        "hentai scene", "hentai story", "hentai video", "hentai movie", "hentai episode", "hentai series"
    ],
    "abbreviations": [
        "pr0n", "s3x", "n00d", "fck", "bj", "hj", "l33t", "p0rn", "h3ntai", "h-ntai", "pnwh",
        "p0rnhwa", "l33tsp34k", "l3wd", "cultur3d", "s3xual"
    ],
    "offensive_slang": [
        "slut", "whore", "tramp", "skank", "cumdumpster", "gangbang", "facial", "golden shower",
        "pegging", "rimming", "rough sex", "dirty talk", "sex chat", "nude pic", "lewd", "titty",
        "twerk", "breasts", "penis", "vagina", "clitoris", "genitals", "sexual", "kamasutra",
        "incest", "pedo", "rape", "sex slave", "bondage", "creampie", "cum inside", "sex doll",
        "sex machine", "latex", "oral sex", "cumshot", "deepthroat", "domination", "submission",
        "handcuffs", "orgy", "roleplay", "sex toy", "voyeur", "cosplay", "adult", "culture",
        "anal", "erotic", "masturbate", "hardcore", "bdsm", "fetish", "lingerie", "milf", "taboo"
    ]
}

# ─────────────────────────────────────────────
# Exceptions: words that may contain "NSFW" substrings but are safe
# ─────────────────────────────────────────────
exception_keywords = [
    "nxivm", "classroom", "assassination", "geass"
]

# ─────────────────────────────────────────────
async def check_anti_nsfw(file_name: str, message: Message) -> bool:
    """
    Checks file name and (if available) message caption/text for NSFW terms.
    Returns True if blocked (NSFW found).
    """
    if not file_name:
        return False

    # Combine filename + message.caption/text for deeper scanning
    text_to_check = file_name.lower()
    if message.caption:
        text_to_check += " " + message.caption.lower()
    if message.text and message.text != file_name:
        text_to_check += " " + message.text.lower()

    # Check exceptions first
    for safe in exception_keywords:
        if safe in text_to_check:
            return False

    # Word-boundary regex to avoid partial matches (e.g., "pass" should not trigger "ass")
    for category, keywords in nsfw_keywords.items():
        for kw in keywords:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, text_to_check):
                await message.reply_text(
                    "🚫 NSFW content detected!\n"
                    "This file cannot be renamed or processed."
                )
                return True

    return False
    
