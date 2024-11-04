from typing import Optional
import json


class LlmInvoker:

    def __init__(self,
                 prompt_messages: Optional[list] = None,
                 stream: Optional[bool] = False,
                 llm: Optional[str] = 'zhipu',
                 ):
        self.prompt_messages = prompt_messages
        self.stream = stream
        self.llm = llm

        if self.llm == 'zhipu':
            from base.llm.zhipu.llm import ZhiPu
            self.client = ZhiPu()

    def invoke(self) -> str:
        return self.client.chat(self.prompt_messages)

    def json(self) -> dict:
        anwser = self.invoke()
        if "{" in anwser and "}" in anwser:
            response = anwser.replace("'", "\"")
            return json.loads(response[response.find("{"): response.rfind("}") + 1])
        else:
            return {}
