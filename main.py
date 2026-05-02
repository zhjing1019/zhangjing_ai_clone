import json
import time
from datetime import datetime
from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL, MEMORY_FILE, YOUR_PERSONA

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 全局聊天上下文
chat_history = []
# 聊天日志保存文件
CHAT_LOG_FILE = "chat_log.json"

def load_my_memory():
    """加载个人风格记忆库"""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_chat_log(role, content):
    """保存单条聊天记录到日志文件"""
    log_item = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "content": content
    }
    try:
        # 读取已有日志
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        logs = []
    
    logs.append(log_item)
    # 写入保存
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dumps(logs, f, ensure_ascii=False, indent=2)

def chat_like_me(user_input):
    global chat_history
    memory = load_my_memory()

    system_prompt = f"""
{YOUR_PERSONA}

我的个人说话风格与思维记忆：
{json.dumps(memory, ensure_ascii=False, indent=2)}

要求：严格模仿我的语气、口头禅、思考逻辑，自然口语化，不要机器人腔调，结合上下文连贯对话。
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7
    )

    reply = response.choices[0].message.content.strip()

    # 存入内存上下文
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": reply})

    # 自动保存到日志文件
    save_chat_log("user", user_input)
    save_chat_log("assistant", reply)

    return reply

if __name__ == "__main__":
    print("✅ AI复制体已启动｜DeepSeek + 上下文记忆 + 自动保存聊天记录")
    print("输入 exit 退出\n")
    while True:
        msg = input("你：")
        if msg.lower() == "exit":
            print("👋 对话结束，聊天记录已自动保存到 chat_log.json")
            break
        reply = chat_like_me(msg)
        print("AI复制体：", reply, "\n")