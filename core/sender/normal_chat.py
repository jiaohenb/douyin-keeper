"""通道A：UID跳转会话，适配新版抖音IM输入框
"""
import time
from ..guard import detect_rate_limit

def send_exist_chat_message(
    nickname: str,
    msg_text: str,
    page,
    context,
    dry_run: bool = False,
) -> tuple[bool, str]:
    page.goto("https://www.douyin.com/douyin-im", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(6000)
    if "passport" in page.url.lower():
        return False, "Cookie失效，需要重新抓取"

    # =====================这里改成对方真实UID数字=====================
    target_uid = "MS4wLjABAAAAjg-B8iucGL8S8m9tcH30ENy38S2xSILfVKKpmceGu3_qqGmqgvnhV58N01DLdeV2"
    chat_url = f"https://www.douyin.com/douyin-im/chat?uid={target_uid}"
    page.goto(chat_url, wait_until="domcontentloaded", timeout=60000)
    # 加长等待，等聊天界面完全渲染
    page.wait_for_timeout(6000)

    if detect_rate_limit(page):
        return False, "检测到验证码/操作频繁"
    try:
        # 新版抖音IM输入框新匹配规则
        input_box = page.locator("div.editor").first
        input_box.wait_for(timeout=20000)
    except Exception:
        return False, "找不到聊天输入框"
    if dry_run:
        return True, "测试成功"
    input_box.click()
    page.keyboard.type(msg_text, delay=150)
    page.keyboard.press("Enter")
    time.sleep(3)
    return True, "消息发送成功"
