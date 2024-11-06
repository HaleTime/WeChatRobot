from wcferry import WxMsg
import re
from db.database import Session
from db.models import Knowledge
import robot

pattern = r'##\s*(.*?)\s*##\s*(.*)'


def learn(msg: WxMsg):
    """
    ## question ## answer
    学习知识
    :param msg: 消息对象
    """

    receiver = msg.roomid if msg.from_group() else msg.sender

    sesstion = Session()
    try:
        message = msg.content
        matches = re.findall(pattern, message)
        question = matches[0][0]
        answer = matches[0][1]
        print(question, answer)

        knowledge = Knowledge(question=question, answer=answer, user_id=receiver)
        sesstion.add(knowledge)
        sesstion.commit()

        robot._robot.reply_text_msg(msg, "好的，我已经记住啦！")
    except Exception as e:
        print(e)
        robot._robot.reply_text_msg(msg, "有点没记住呢，能再教我一次么？")
    finally:
        sesstion.close()


# 校验函数
def validate_format(data):
    # 正则表达式：确保格式是 ##内容 ##内容
    p = r'^##\s*\S+\s*##\s*\S+$'

    # 使用 re.match 来校验
    return re.match(p, data)


def init_knowledge():
    sesstion = Session()
    try:
        knowledges = [
            Knowledge(question="怎么进行知识学习",
                      answer="您需要按照格式##{question} ##{answer}的格式发送给我，然后我就会记住的~",
                      type=0,
                    ),

            Knowledge(question="你都能做些什么？你有哪些功能？",
                      answer="1. 定时提醒\n2. 学习知识",
                      type=0,
                      ),
        ]
        sesstion.add_all(knowledges)
        sesstion.commit()

    except Exception as e:
        print(e)
    finally:
        sesstion.close()


if __name__ == '__main__':
    # init_knowledge()
    sesstion = Session()
    all = sesstion.query(Knowledge).filter(Knowledge.type == 0).all()
    for a in all:
        print(a.question)
        print(a.answer)
