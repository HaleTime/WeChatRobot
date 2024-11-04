from zhipuai import ZhipuAI
from configuration import Config
from base.llm.llm_model import LlmModel


class ZhiPu(LlmModel):
    def __init__(self) -> None:
        config = Config().ZhiPu
        self.api_key = config.get("api_key")
        self.model = config.get("model", "glm-4")  # 默认使用 glm-4 模型
        self.client = ZhipuAI(api_key=self.api_key)

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        resp_msg = response.choices[0].message
        print(resp_msg)
        answer = resp_msg.content
        return answer
