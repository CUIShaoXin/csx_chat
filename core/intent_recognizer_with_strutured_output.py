from langchain_community.chat_models import ChatTongyi
from langchain_core.prompt_values import ChatPromptValue
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Any
from core.prompt import INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT
from langchain_core.output_parsers import StrOutputParser


class IntentResult(BaseModel):
    intents: list[str] = Field(description="意图列表，每个元素为一个意图名称")
    slots: dict[str, Any] = Field(description="slot值字典，键为slot值")  # 插槽
    confidence: float = Field(description="置信度分数")  # 置信度


class IntentRecognizer:

    def __init__(self, llm: ChatTongyi):
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT),
            ("ai", "上下文内容：{chat_history}"),
            ("human", "用户输入：{user_input}")
        ])
        self.__llm = llm.with_structured_output(IntentResult)
        self.__chain = self.__prompt | self.__llm

    def recognize(self, user_input: str, chat_history: str | None = None) -> IntentResult:
        chat_history = chat_history if chat_history else ""
        result = self.__chain.invoke(input={"user_input": user_input, "chat_history": chat_history})

        if result is None:
            return IntentResult(
                intents=["general"],
                slots={},
                confidence=0.0,
            )
        return result