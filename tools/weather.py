from datetime import datetime

schame = {
    "name": "get_weather",
    "description": "查询天气",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "description": f"默认当前日期{datetime.today().strftime('%Y-%m-%d')}, 格式: 2023-01-01",
                "type": "string",
            },
            "city": {
                "description": "城市",
                "type": "string",
            },
        },
        "required": ["date", "city"]
    },
}


def get_weather(date: str, city: str) -> str:
    """模拟发送天气预报
    """

    # # 获取接收人
    # receivers = ["filehelper"]
    #
    # # 获取天气，需要自己实现，可以参考 https://gitee.com/lch0821/WeatherScrapy 获取天气。
    # report = "这就是获取到的天气情况了"
    #
    # for r in receivers:
    #     robot.sendTextMsg(report, r)
    #     # robot.sendTextMsg(report, r, "notify@all")   # 发送消息并@所有人

    return f'{date}{city}是晴天'
