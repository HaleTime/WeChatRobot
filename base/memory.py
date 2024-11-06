from typing import Dict
from collections import deque


class Conversation:

    def __init__(self, receiver: str, from_group: bool, current_tool: str = "other"):
        """
        :param receiver: wxid或者群id
        :param from_group: 是否为群
        """

        self.messages = deque(maxlen=20)
        self.receiver = receiver
        self.from_group = from_group
        self.current_tool = current_tool

        conversation_list[receiver] = self

    def update_message(self, message: str, user: str, tool: str = "other"):
        """
        :param message: 说话内容
        :param user: wxid 或者 me
        """
        self.messages.append({"user": user, "message": message, "tool": tool})

    def get_prompt_messages(self, tool: str = None) -> list:
        if tool:
            return [
                {
                    "role": "user" if "me" == _.get("user") else "assistant",
                    "content": _.get("message", "")
                }
                for _ in self.messages if _.get("tool") == tool
            ]
        return [
            {
                "role": "user" if "me" == _.get("user") else "assistant",
                "content": _.get("message", "")
            }
            for _ in self.messages
        ]

    def change_tool(self, tool: str):
        self.current_tool = tool


conversation_list: Dict[str, Conversation] = {}
