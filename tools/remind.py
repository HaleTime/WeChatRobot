from threading import Timer
import robot
from datetime import datetime
from wcferry import WxMsg
from base.llm.llm_invoker import LlmInvoker
from base.memory import conversation_list, Conversation

remind_me_tool = {
    "name": "remind_me",
    "description": "在指定时间提醒你",
}


def remind_me(msg: WxMsg):
    receiver = msg.roomid if msg.from_group() else msg.sender
    conversation = conversation_list.get(receiver, Conversation(receiver=receiver, from_group=msg.from_group()))

    messages = conversation.get_prompt_messages()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt = f"""根据下面这句话提取出时间和提醒的内容，用json的形式返回
最后的问题:
{msg.content}

返回格式:
{{
    "time": <当前时刻为{date},要提取的时间, 格式为yyyy-MM-dd hh:mm>,
    "msg": <提醒内容>
}}
"""
    messages.append({"role": "user", "content": prompt})
    llm = LlmInvoker(prompt_messages=messages)

    result = llm.json()
    time = result.get("time")
    message = result.get("msg")

    now = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    target_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    # 计算时间差
    time_difference = target_time - now
    if time_difference.total_seconds() < 0:
        robot._robot.reply_text_msg(msg, "时间已经过去了，无法设置提醒")
    else:
        time = time_difference.total_seconds()
    print(f'time: {time}')

    def send_message():
        for _ in range(3):
            robot._robot.reply_text_msg(msg, message)
            time.sleep(1)

    timer = Timer(int(time), send_message)
    timer.start()
    robot._robot.reply_text_msg(msg, "好的，稍后我会提醒你的")
