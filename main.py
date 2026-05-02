import json
from openai import OpenAI  # DeepSeek 兼容 OpenAI 接口
from config import API_KEY, BASE_URL, MODEL, MEMORY_FILE, YOUR_PERSONA

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def load_my_memory():
    """加载你的性格/说话风格记忆"""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def chat_like_me(user_input):
    """让AI完全模仿你说话"""
    memory = load_my_memory()
    
    prompt = f"""
{YOUR_PERSONA}

我的记忆（说话风格 + 思维方式）：
{json.dumps(memory, ensure_ascii=False, indent=2)}

现在别人对我说：{user_input}
请你严格模仿我的风格来回复，不要像机器人，自然一点。
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("✅ 你的AI复制体已启动，输入 exit 退出")
    while True:
        msg = input("你：")
        if msg.lower() == "exit":
            print("👋 结束对话")
            break
        
        reply = chat_like_me(msg)
        print("AI复制体：", reply, "\n")