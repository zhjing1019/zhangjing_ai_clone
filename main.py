import json
from datetime import datetime
from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL, MEMORY_FILE, YOUR_PERSONA

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# 文件路径
CHAT_HISTORY_FILE = "chat_history.json"
CHAT_LOG_FILE = "chat_log.json"

# 全局对话上下文
chat_history = []

def load_my_memory():
    """加载个人风格记忆库"""
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def load_saved_chat_history():
    """启动时加载保存的对话上下文"""
    global chat_history
    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
            chat_history = json.load(f)
        print("✅ 已加载上次对话上下文")
    except:
        chat_history = []
        print("ℹ️ 暂无历史对话，开启新会话")

def save_chat_history():
    """保存当前对话上下文到文件"""
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

def save_chat_log(role, content):
    """保存带时间戳的聊天日志"""
    log_item = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "content": content
    }
    try:
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        logs = []
    logs.append(log_item)
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

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

    # 追加到内存上下文
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": reply})

    # 保存上下文 & 聊天日志
    save_chat_history()
    save_chat_log("user", user_input)
    save_chat_log("assistant", reply)

    return reply

if __name__ == "__main__":
    print("✅ AI复制体启动｜DeepSeek + 上下文记忆 + 自动存日志 + 重启续聊")
    # 程序启动自动加载历史对话
    load_saved_chat_history()
    print("输入 exit 退出，输入 clear 清空本次对话记忆\n")

    while True:
        msg = input("你：")
        if msg.lower() == "exit":
            print("👋 对话结束，上下文与日志已自动保存")
            break
        # 新增清空记忆命令
        if msg.lower() == "clear":
            chat_history = []
            save_chat_history()
            print("🧹 已清空历史对话记忆\n")
            continue
        reply = chat_like_me(msg)
        print("AI复制体：", reply, "\n")