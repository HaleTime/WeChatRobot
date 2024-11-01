from threading import Timer
import robot
from datetime import datetime

remind_me_schema = {
    "name": "remind_me",
    "description": "在指定时间或者指定时间后提醒你",
    "parameters": {
        "type": "object",
        "properties": {
            "time": {
                "description": f"多久后提醒你，单位: h/m/s,例如 1h 5m 30s\n 在某个时刻提醒你，例如 14:20",
                "type": "string",
            },
            # "absolute_time": {
            #     "description": f"在某个时刻提醒你，例如 14:20",
            #     "type": "string",
            # },
            "msg": {
                "description": "提醒内容",
                "type": "string",
            },
        },
        "required": ["time", "msg"]
    },
}


def remind_me(timestr: str, msg: str, receiver: str, at_list: str, **kwargs):
    time = 1
    if timestr and timestr not in {'0s', '0m', '0h'}:
        unit = timestr[-1]
        _time = int(timestr[:-1])
        if unit == "h":
            time = _time * 3600
        elif unit == "m":
            time = _time * 60
        else:
            time = _time
    # elif absolute_time:
    #     now = datetime.now()
    #     target_time = datetime.strptime(absolute_time, "%H:%M")
    #     target_time = target_time.replace(year=now.year, month=now.month, day=now.day)
    #
    #     # 计算时间差
    #     time_difference = target_time - now
    #     if time_difference.total_seconds() < 0:
    #         return "时间已经过去了，无法设置提醒"
    #     else:
    #         time = time_difference.total_seconds()
    print(f'time: {time}')
    timer = Timer(time, robot._robot.sendTextMsg, args=(msg, receiver, at_list))
    timer.start()

    return "好的，稍后我会提醒你的"
