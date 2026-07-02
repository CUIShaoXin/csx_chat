import json
import re
from dataclasses import dataclass
from typing import Any

from langchain_community.chat_models import ChatTongyi

from CSX_Chat.core.prompt import INTENT_RECOGNIZE_PROMPT
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser



@dataclass(frozen=True)  # 装饰器告诉我这是个不可变类
class IntentResult:
    intents: list[str]
    slots: dict[str, Any]  # 插槽
    confidence: float     # 置信度


class IntentRecognizer:

    def __init__(self, llm: ChatTongyi):
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", INTENT_RECOGNIZE_PROMPT),
            ("ai", "上下文内容：{chat_history}"),
            ("human", "用户输入：{user_input}")
        ])
        self.__llm = llm
        self.__chain = self.__prompt | self.__llm | StrOutputParser()

    def recognize(self, user_input: str, chat_history: str | None = None) -> IntentResult:

        chat_history = chat_history if chat_history else ""
        result = self.__chain.invoke(input={"user_input": user_input, "chat_history": chat_history})

        #将大模型输出的 str 转化成json
        data = self.__parse_str_to_json(result)

        #解析intents意图
        intents = data.get("intents")
        # 意图的健壮性测试
        if not isinstance(intents, list):
            intent = data.get("intent")
            intents = [intents] if isinstance(intents,str) else []
        # 解析slots插槽
        slots =data.get("slots") if isinstance(data.get("slots"),dict) else {}
        #解析confidence置信度，转化成float
        try:
            confidence = float(data.get("confidence"))
        except:
            confidence = 0.0
        confidence =max(0.0,min(1.0,confidence))

        #完成判断后
        return IntentResult(intents=intents, slots=slots, confidence=confidence)



        
    #不能用jsonoutputparser 因为黑盒的原因报错的话找不到错误
    #设置方法：去把大模型输出str 转化为 json
    def __parse_str_to_json(self, text:str)->dict[str, Any]:
        #如果输入的str文本是空的话，那么就返回"闲聊模式"
        if not text or not text.strip():
            return {"intents": ["general"], "slots": {}, "confidence": 0.0}

        text = text.strip()
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError:
            pass

        # 如果上面的解析失败，则尝试利用正则表达式 提取json字符串
        find_text = re.search(r"{{.*}}", text,re.DOTALL)
        if find_text:
            try:
                return json.loads(find_text.group(0))
            except json.JSONDecodeError:
                pass
        #如果还是没有找到json字符串，那么返回默认值
        return {"intents": ["general"], "slots": {}, "confidence": 0.0}