import sys
from pathlib import Path
from loguru import logger


"""
日志
"""
def handle_logger():
    # log 目录
    log_path: Path = Path(__file__).parent.parent / "log"

    # 日志格式
    LOG_FORMATTER: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green>| <level>{level: <5}</level>|<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    # 设置日志文件名格式，将日期添加到文件名中
    log_file_info = log_path / "info.log"
    log_file_error = log_path / "error.log"

    # 移除默认的输出处理器
    logger.remove()

    # 添加控制台输出处理器
    logger.add(
        sys.stdout,
        level="DEBUG",
        format=LOG_FORMATTER,
    )

    # 添加 info 日志处理器
    logger.add(
        log_file_info,
        rotation="00:00",
        level="INFO",
        encoding="utf-8",
        format=LOG_FORMATTER,
        enqueue=True,  # 进程安全
    )

    # 添加 error 日志处理器
    logger.add(
        log_file_error,
        rotation="00:00",
        level="ERROR",
        encoding="utf-8",
        format=LOG_FORMATTER,
        enqueue=True,
    )

    return logger


log = handle_logger()


