import datetime

def readable_time(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds))
  
