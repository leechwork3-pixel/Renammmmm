import time
import datetime
from pyrogram.errors import FloodWait

# ===== New progress function from current bot =====
async def progress_for_pyrogram(current, total, ud_type, message, start):
    """
    Progress callback for Pyrogram's upload/download methods.
    """
    now = time.time()
    diff = now - start
    if total != 0 and (round(diff % 5.0) == 0 or current == total):  # Update every 5s or on completion
        percent = current * 100 / total
        speed = current / diff if diff > 0 else 0
        eta = time_formatter(round((total - current) / speed)) if speed > 0 else "0s"

        try:
            await message.edit_text(
                text=f"{ud_type}\n"
                     f"📊 **Progress:** {percent:.2f}%\n"
                     f"📦 **Size:** {humanbytes(current)} / {humanbytes(total)}\n"
                     f"⚡ **Speed:** {humanbytes(speed)}/s\n"
                     f"⏳ **ETA:** {eta}"
            )
        except FloodWait as e:
            time.sleep(e.value)
        except Exception:
            pass


# ===== From older utils.py =====
def readable_time(seconds: int) -> str:
    """
    Converts seconds to a human-readable time format (e.g., HH:MM:SS).
    """
    return str(datetime.timedelta(seconds=int(seconds)))


def format_file_size(size_bytes: int) -> str:
    """
    Convert file size in bytes into a human-readable string in KB, MB, GB, etc.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"


def eta_format(seconds: int) -> str:
    """
    Format ETA seconds to a friendly string, showing days, hours, minutes, seconds.
    """
    if seconds <= 0:
        return "0s"
    td = datetime.timedelta(seconds=int(seconds))
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    if secs: parts.append(f"{secs}s")
    return ' '.join(parts)


def calc_speed(bytes_transferred: int, elapsed_seconds: float) -> str:
    """
    Calculate transfer speed in MB/s given bytes transferred and elapsed time.
    """
    if elapsed_seconds <= 0:
        return "0.00 MB/s"
    speed = (bytes_transferred / 1024 / 1024) / elapsed_seconds
    return f"{speed:.2f} MB/s"


# ===== From current helpers for compatibility =====
def humanbytes(size: float) -> str:
    """
    Convert bytes to a human-readable string with units.
    """
    if not size:
        return ""
    power = 1024
    n = 0
    power_labels = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size >= power and n < 4:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"


def time_formatter(seconds: int) -> str:
    """
    Format seconds into a digital clock format.
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"
        
