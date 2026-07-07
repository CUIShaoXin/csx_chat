from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent


# 1.创建 tool
@tool
def get_goods_info_by_id(goods_id: int) -> str | None:
    """
    根据商品goods_id去查询商品信息
    :param goods_id: 商品id
    :return: 查询到的商品信息，没查询到就返回空
    """
    goods_info = {
        1: "爱疯手机",
        2: "华为电脑"
    }
    if goods_id not in goods_info:
        print(f"id为{goods_id}的商品不存在")
        return None
    goods = goods_info[goods_id]
    print(f"id为{goods_id}的商品为：{goods}")
    return goods


# 2. 创建 Agent
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),  # 给 Agent 提供大脑
    tools=[get_goods_info_by_id],  # 给 Agent 提供工具
    system_prompt="你是一个商品信息查询助手，如果用户传入商品ID，请你帮他查询是什么商品"
)

# 3.调用 agent 去帮我们查询商品信息
result = agent.invoke({
    "messages": [{"role": "user", "content": "商品id为1，这个是一个什么商品"}]
})

# 4.打印结果
print(type(result))  # <class 'dict'>
print(result)
print(result['messages'])
print(len(result['messages']))

print('\n' + '=' * 20)
for msg in result['messages']:
    print(f"消息类型：{type(msg).__name__}，消息内容：{msg}")