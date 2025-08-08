nsfw_keywords = [
    "porn", "sex", "nude", "naked", "fuck", "boobs", "xxx", "pussy", "dick", "ass", 
    "cum", "bdsm", "shemale", "fetish", "milf", "hentai", "18+", "loli", "rape",
    "erotic", "lewd", "tramp", "creampie", "tits", "orgasm", "vagina", "clitoris",
    "pedo", "bondage", "masturbate", "masturbation"
]

exception_list = ["assassin", "assault", "classroom", "geass"]


async def check_anti_nsfw(file_name: str, message):
    if not file_name:
        return False

    lower = file_name.lower()

    for exception in exception_list:
        if exception in lower:
            return False

    for word in nsfw_keywords:
        if word in lower:
            await message.reply_text("🚫 File not allowed due to NSFW content.")
            return True

    return False
    
