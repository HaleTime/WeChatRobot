from abc import abstractmethod, ABC


class LlmModel(ABC):
    """
    暂时只应用于系统内部支持的智能工具生成器，自定义的以后按需看是否要合并成一个
    """

    @abstractmethod
    def chat(self, *args, **kwargs):
        pass
