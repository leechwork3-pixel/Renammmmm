import time
import datetime
from pyrogram.errors import FloodWait

# ─────────────────────────────────────────────
# Progress callback for Pyrogram's upload/download
# ─────────────────────────────────────────────
async def progress_for_pyrogram(current, total, ud_type, message, start):
    """
    Async progress callback for Pyrogram media downloads/uploads.
    Updates the message with progress %, speed, ETA, and size info every 5 seconds.

    Args:
        current (int): Bytes transferred so far.
        total (int): Total number of bytes.
        ud_type (str): Upload type description (e.g., "Uploading", "Downloading").
        message (pyrogram.types.Message): The message to be edited.
        start (float): Timestamp of when the transfer started.
    """
    now = time.time()
    diff = now - start
    if total > 0 and (round(diff) % 5 == 0 or current == total):
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

# ─────────────────────────────────────────────
# Convert seconds to HH:MM:SS
# ─────────────────────────────────────────────
def readable_time(seconds: int) -> str:
    """
    Convert seconds to HH:MM:SS human-readable time string.

    Args:
        seconds (int): Duration in seconds.

    Returns:
        str: Formatted time string.
    """
    return str(datetime.timedelta(seconds=int(seconds)))

# ─────────────────────────────────────────────
# Bytes to human-readable file size
# ─────────────────────────────────────────────
def format_file_size(size_bytes: int) -> str:
    """
    Convert file size into KB/MB/GB readable string.

    Args:
        size_bytes (int): Size in bytes.

    Returns:
        str: Human-readable size string.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"

# ─────────────────────────────────────────────
# ETA in d/h/m/s format
# ─────────────────────────────────────────────
def eta_format(seconds: int) -> str:
    """
    Convert ETA in seconds to a formatted string like: 1h 5m, 2d 3h 45s

    Args:
        seconds (int): Estimated time in seconds.

    Returns:
        str: Readable ETA string.
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

# ─────────────────────────────────────────────
# Calculate transfer speed in MB/s
# ─────────────────────────────────────────────
def calc_speed(bytes_transferred: int, elapsed_seconds: float) -> str:
    """
    Calculate speed in MB/s.

    Args:
        bytes_transferred (int): Bytes transferred so far.
        elapsed_seconds (float): Elapsed duration.

    Returns:
        str: Speed formatted as "X.XX MB/s"
    """
    if elapsed_seconds <= 0:
        return "0.00 MB/s"
    speed = (bytes_transferred / 1024 / 1024) / elapsed_seconds
    return f"{speed:.2f} MB/s"

# ─────────────────────────────────────────────
# Convert bytes to human-readable using KiB, MiB
# ─────────────────────────────────────────────
def humanbytes(size: float) -> str:
    """
    Convert byte count to human-readable form (e.g., 1.32 MiB)

    Args:
        size (float): Size in bytes

    Returns:
        str: Humanized string with unit
    """
    if not size:
        return ""
    power = 1024
    n = 0
    Dic_powerN = {0: '', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size >= power and n < 4:
        size /= power
        n += 1
    return f"{round(size, 2)} {Dic_powerN[n]}B"

# ─────────────────────────────────────────────
# Time in seconds to HH:MM:SS or MM:SS
# ─────────────────────────────────────────────
def time_formatter(seconds: int) -> str:
    """
    Format time in seconds to a digital clock format (H:MM:SS or MM:SS)

    Args:
        seconds (int): Duration in seconds

    Returns:
        str: Formatted time string
    """
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{hours}:{mins:02d}:{secs:02d}"
    else:
        return f"{mins:02d}:{secs:02d}"

