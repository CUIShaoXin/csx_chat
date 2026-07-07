from langchain_community.chat_models import ChatTongyi
from langchain.tools import tool
from langchain_core.messages import ToolMessage

# 1.创建模型客户端
llm = ChatTongyi(model="qwen3-max")


# 2.给 LLM 添加工具
# 2.1.创建工具
@tool
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    return f"{location}的天气是100摄氏度，请你注意防晒"


# 2.2.将工具绑定到llm
tools = [get_weather]
model_with_tools = llm.bind_tools(tools=tools)

# 3.调用模型
# user_input = "北京的天气怎么样？"
user_input = "波士顿和东京的天气怎么样？"
messages = [
    ("system", "你是一个有好的天气查询助手"),
    ("human", user_input)
]
result = model_with_tools.invoke(messages)

# 4. 根据 tool_calls 调用工具
# key：方法名字，value：方法
tool_map = {tool.name: tool for tool in tools}

if result.tool_calls:
    # 关键步骤：将 AI 的响应添加到消息历史中
    messages.append(result)

    # 解析result的tool_calls
    for tool_call in result.tool_calls:
        tool_name = tool_call['name']
        tool_args = tool_call['args']
        tool_id = tool_call['id']

        tool_func = tool_map.get(tool_name)
        if tool_func:
            try:
                tool_result = tool_func.invoke(tool_args)
                print(f"调用工具 '{tool_name}' 成功，结果: {tool_result}")
                # 创建 ToolMessage 并将结果添加到消息历史
                tool_message = ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_id
                )
                messages.append(tool_message)
            except Exception as e:
                # todo
                tool_message = ToolMessage(
                    content=f"工具调用失败: {str(e)}",
                    tool_call_id=tool_id
                )
                messages.append(tool_message)
        else:
            print(f"未找到工具：{tool_name}")
            tool_message = ToolMessage(
                content=f"未找到工具: {tool_name}",
                tool_call_id=tool_id
            )
            messages.append(tool_message)

else:
    print("没有需要调用的工具")
    print(result.content)


# 5. 再次调用模型，获取最终回答
print("\n" + "=" * 50)
print("消息历史:")
for msg in messages:
    print(f"{type(msg).__name__}: {msg}")
print("=" * 50 + "\n")


result = model_with_tools.invoke(messages)
print(result.content)
"""
北京的天气显示为100摄氏度，这显然不太正常，可能是数据错误。通常北京的气温不会达到如此高的程度。
不过，如果天气确实炎热，请务必注意防晒、
多喝水，并尽量避免在烈日下长时间活动。建议查看权威天气预报以获取准确信息！
"""
"""
user_input = "波士顿和东京的天气怎么样？" async
tool_calls=[
{'name': 'get_weather', 'args': {'location': '波士顿'}, 'id': 'call_200b5274771d48baacaf1c2d', 'type': 'tool_call'},
{'name': 'get_weather', 'args': {'location': '东京'}, 'id': 'call_b8ed9aeaf31f4a9fa2799b35', 'type': 'tool_call'}
 ]
"""


