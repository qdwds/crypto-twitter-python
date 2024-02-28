
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime, timedelta
import os

def handle_logger():
    # log 目录
    log_path: Path = Path(__file__).parent.parent / "logs"

    # 日志格式
    LOG_FORMATTER: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green>| <level>{level: <5}</level>|<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # 设置日志文件名格式，将日期添加到文件名中
    log_file = log_path / "logs_{time:YYYY-MM-DD}.log"

    # 移除默认的输出处理器
    logger.remove()

    # 添加控制台输出处理器
    logger.add(
        sys.stdout,
        level="DEBUG",
        format=LOG_FORMATTER,
    )

    # 添加日志处理器，写入同一个日志文件，以日期为后缀
    logger.add(
        log_file,
        rotation="00:00",
        level="INFO",
        encoding="utf-8",
        format=LOG_FORMATTER,
        enqueue=True,  # 进程安全
    )

    # 删除7天前的日志
    delete_old_logs(log_path, days_to_keep=7)

    return logger

def delete_old_logs(logs_dir, days_to_keep):
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(days=days_to_keep)

    for filename in os.listdir(logs_dir):
        filepath = os.path.join(logs_dir, filename)

        if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time.timestamp():
            os.remove(filepath)
            print(f"Deleted old log file: {filepath}")

log = handle_logger()