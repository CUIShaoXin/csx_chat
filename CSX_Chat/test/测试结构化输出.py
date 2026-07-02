

from CSX_Chat.core import IntentRecognizer

from langchain_community.chat_models import ChatTongyi


if __name__=="__main__":
    llm = ChatTongyi(model="qwen3-max")
    recognizer =IntentRecognizer(llm)

    result = recognizer.recognize("我的订单号是022222123321321")
    print(result)

    result = recognizer.recognize("我的订单号是022222123321321","human: 我想退货 \n ai:请你提供你的订单号")
    print(result)