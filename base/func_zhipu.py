from zhipuai import ZhipuAI
from prompt import SYSTEM_PROMPT
import tools
import json


class ZhiPu:
    def __init__(self, conf: dict) -> None:
        self.api_key = conf.get("api_key")
        self.model = conf.get("model", "glm-4")  # 默认使用 glm-4 模型
        self.client = ZhipuAI(api_key=self.api_key)
        self.converstion_list = {}

    @staticmethod
    def value_check(conf: dict) -> bool:
        if conf and conf.get("api_key"):
            return True
        return False

    def __repr__(self):
        return 'ZhiPu'

    def get_answer(self, msg: str, receiver: str, at_list: str = "", **kwargs) -> str:
        self._update_message(receiver, str(msg), "user")

        print(self.converstion_list[receiver])
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.converstion_list[receiver],
            tools=tools.tools_schema,
        )

        resp_msg = response.choices[0].message
        print(resp_msg)
        if resp_msg.tool_calls:
            tool_call_id = resp_msg.tool_calls[0].id
            tool_call = resp_msg.tool_calls[0]
            tool_call_args = json.loads(tool_call.function.arguments)
            tool_call_name = tool_call.function.name

            if tool_call_name == "get_weather":
                date = tool_call_args.get("date")
                city = tool_call_args.get("city")
                weather = tools.get_weather(date, city)
                self._update_message(receiver, weather, "tool", tool_call_id=tool_call_id)
                print(self.converstion_list[receiver])
                response1 = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.converstion_list[receiver],
                )
                resp_msg1 = response1.choices[0].message
                print(2, resp_msg1)
                answer1 = resp_msg1.content
                return answer1
            if tool_call_name == "remind_me":
                time = tool_call_args.get("time")
                # absolute_time = tool_call_args.get("absolute_time")
                msg = tool_call_args.get("msg")
                answer = tools.remind_me(time, msg, receiver=receiver, at_list=at_list,
                                         from_group=kwargs.get("from_group", False))
                self._update_message(receiver, answer, "assistant")
                return answer

        answer = resp_msg.content
        self._update_message(receiver, answer, "assistant")
        return answer

    def _update_message(self, wxid: str, msg: str, role: str, **kwargs) -> None:
        if wxid not in self.converstion_list.keys():
            self.converstion_list[wxid] = []
            system = {"role": 'system', "content": SYSTEM_PROMPT}
            self.converstion_list[wxid].append(system)

        content = {"role": role, "content": str(msg), **kwargs}
        self.converstion_list[wxid].append(content)


if __name__ == "__main__":
    from configuration import Config

    config = Config().ZhiPu
    if not config:
        exit(0)

    zhipu = ZhiPu(config)
    rsp = zhipu.get_answer("5秒后提醒我吃饭", 1)
    print(rsp)
