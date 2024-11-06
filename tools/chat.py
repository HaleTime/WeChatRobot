from wcferry import WxMsg
from base.llm.llm_invoker import LlmInvoker
from base.memory import conversation_list, Conversation
from prompt import SYSTEM_PROMPT
import robot
from db.database import Session
from db.models import Knowledge
from sqlalchemy import or_


def chat(msg: WxMsg):
    sesstion = Session()
    try:
        receiver = msg.roomid if msg.from_group() else msg.sender
        message = msg.content

        conversation = conversation_list.get(receiver, Conversation(receiver=receiver, from_group=msg.from_group()))
        prompt_messages = [{"role": 'system', "content": SYSTEM_PROMPT}]
        prompt_messages.extend(
            [{
                "role": "user" if _message.get("user") == "me" else "assistant",
                "content": _message.get("message", "")
            }
                for _message in conversation.messages])

        knowledges = sesstion.query(Knowledge).filter(or_(Knowledge.type == 0, Knowledge.user_id == receiver)).all()
        prompt = f"""

"""
        prompt_messages.append({"role": "user", "content": message})
        answer = LlmInvoker(prompt_messages=prompt_messages).invoke()
        conversation.update_message(answer, "me", "other")

        robot._robot.reply_text_msg(msg, answer)
    except Exception as e:
        print(e)
    finally:
        sesstion.close()
