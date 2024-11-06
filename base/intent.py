from wcferry import WxMsg

from base.llm.llm_invoker import LlmInvoker
from base.memory import conversation_list, Conversation
from tools import tools
import logging

log = logging.getLogger("intent")


def intent_identify(msg: WxMsg):
    receiver = msg.sender
    message = msg.content

    print(f"{receiver}: {message}")

    conversation = conversation_list.get(receiver, Conversation(receiver=receiver, from_group=msg.from_group()))
    prompt_messages = conversation.get_prompt_messages()

    prompt = f"""根据下面的步骤推理问题:
1. 通读对话内容，分析用户最后一句话的意图
2. 根据用户意图，在tools里面选择合适的tool
3. 如果没有合适的tool，请返回{{"name": "other"}}

用户最后一句话:
{msg.content}

tools:

按照下面json返回结果:
{{"name": <tool的name>"}}
"""

    prompt_messages.append({"role": "user", "content": prompt})
    print(prompt_messages)

    llm = LlmInvoker(prompt_messages)
    result = llm.json()
    tool_result = result.get('name', 'other')
    conversation.update_message(message, receiver, tool=tool_result)
    conversation.change_tool(tool_result)
    print(f"意图识别结果: {result}")
    return tool_result
