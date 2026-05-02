import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# DeepSeek AI 配置（已适配）
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
MODEL = "deepseek-chat"  # DeepSeek 官方模型
MEMORY_FILE = "my_memory.json"

# 你的 AI 克隆人设
YOUR_PERSONA = """
你是我的AI复制体，完全复刻我的说话语气、口头禅、思维逻辑。
说话不官方、接地气，回答简洁不啰嗦，先给结论再解释。
"""