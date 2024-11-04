from wcferry import WxMsg
from base.llm.llm_invoker import LlmInvoker
from base.memory import conversation_list, Conversation
from prompt import SYSTEM_PROMPT
import robot


def chat(msg: WxMsg):
    receiver = msg.roomid if msg.from_group() else msg.sender
    message = msg.content
    conversation = conversation_list.get(receiver, Conversation(receiver=receiver, from_group=msg.from_group()))
    prompt_messages = [{"role": 'system', "content": SYSTEM_PROMPT}]
    prompt_messages.extend(
        [{"role": "user" if _message.get("user") == "me" else "assistant", "content": _message.get("message", "")} for
         _message in conversation.messages])
    prompt_messages.append({"role": "user", "content": message})
    answer = LlmInvoker(prompt_messages=prompt_messages).invoke()
    conversation.update_message(answer, "me")

    robot._robot.reply_text_msg(msg, answer)
