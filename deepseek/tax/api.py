from openai import OpenAI

# 初始化 DeepSeek 客户端
client = OpenAI(api_key="sk-d0a0e5d5358e4d579ac8c5afc2961c37", base_url="https://api.deepseek.com")

# 初始化对话上下文
messages = [
    {
        "role": "system",
        "content": "你好，现在你是一名税务和发票（包括进项发票销项发票）专家，并且是一个企业信息化专家,而且是资深开发程序员和架构师。",
    }
]

# 连续对话函数
def chat_with_ai():
    print("欢迎使用 DeepSeek 税务和发票助手！输入 '退出' 结束对话。")
    while True:
        # 获取用户输入
        user_input = input("你: ")
        if user_input.lower() == "退出":
            print("对话结束，再见！")
            break

        # 将用户输入添加到对话上下文
        messages.append({"role": "user", "content": user_input})

        # 调用 API 获取模型回复
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=True,
        )

        # 获取模型回复
        ai_response = response.choices[0].message.content

        # 将模型回复添加到对话上下文
        messages.append({"role": "assistant", "content": ai_response})

        # 打印模型回复
        print(f"DeepSeek: {ai_response}")

# 启动对话
if __name__ == "__main__":
    chat_with_ai()