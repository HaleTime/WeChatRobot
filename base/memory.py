from typing import Dict
from collections import deque


class Conversation:

    def __init__(self, receiver: str, from_group: bool):
        """
        :param receiver: wxid或者群id
        :param from_group: 是否为群
        """

        self.messages = deque(maxlen=10)
        self.receiver = receiver
        self.from_group = from_group
        conversation_list[receiver] = self

    def update_message(self, message: str, user: str):
        """
        :param message: 说话内容
        :param user: wxid 或者 me
        """
        self.messages.append({"user": user, "message": message})

    def get_prompt_messages(self) -> list:
        return [
            {
                "role": "user" if "me" == _.get("user") else "assistant",
                "content": _.get("message", "")
            }
            for _ in self.messages
        ]


conversation_list: Dict[str, Conversation] = {}
