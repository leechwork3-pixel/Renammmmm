import datetime

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
    
