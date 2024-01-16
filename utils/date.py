from datetime import datetime, timedelta
import pytz  # 使用 pytz 模块处理时区信息


"""日期格式化"""
def format_date(time):
    # 将输入字符串解析为datetime对象（默认为UTC时间）
    input_date_utc = datetime.strptime(time, "%b %d, %Y · %I:%M %p UTC")

    # 定义UTC时区
    utc_timezone = pytz.timezone("UTC")

    # 将UTC时间转换为北京时间
    beijing_timezone = pytz.timezone("Asia/Shanghai")
    input_date_beijing = input_date_utc.replace(tzinfo=utc_timezone).astimezone(beijing_timezone)

    return input_date_beijing.strftime("%Y-%m-%d %H:%M:%S")

