from pyrogram import Client, filters
from pyrogram.types import Message

# NSFW keyword categories
nsfw_keywords = {
    "general": [
        # (same as your provided list)
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
        "oral sex", "butt", "slut", "whore", "tramp", "skank", "cumdumpster", "cultured",
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

# List of safe exceptions (useful terms that shouldn't trigger false positive matches)
exception_keywords = ["nxivm", "classroom", "assassination", "geass"]

async def check_anti_nsfw(file_name: str, message: Message) -> bool:
    """
    Checks a file name for NSFW terms. Returns True if blocked.
    """
    if not file_name:
        return False

    name_lower = file_name.lower()

    # Check exceptions first
    for safe in exception_keywords:
        if safe in name_lower:
            return False  # Allow it

    # Run NSFW keyword checks
    for category, keywords in nsfw_keywords.items():
        for kw in keywords:
            if kw in name_lower:
                await message.reply_text("🚫 NSFW content detected! Renaming of this file is not allowed.")
                return True

    return False
    
