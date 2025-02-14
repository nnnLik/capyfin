from datetime import datetime

def convert_to_timestamp(time_str: str) -> int:
    """Конвертирует строку времени в timestamp (миллисекунды)."""
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp() * 1000)
