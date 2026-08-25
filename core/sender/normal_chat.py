"""通道A：直接会话链接跳转发送，绕过左侧会话列表加载问题
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
    # 重点：抖音im会话格式 https://www.douyin.com/douyin-im/chat?uid=这里填对方抖音UID
    # 你需要手动拿到好友的UID替换或者后续适配
    # 先打开im主页
    page.goto("https://www.douyin.com/douyin-im", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(5000)
    if "passport" in page.url.lower():
        return False, "Cookie失效，需要重新抓取"

    # ============ 这里要你替换成目标好友的真实UID ============
    target_uid = "MS4wLjABAAAAjg-B8iucGL8S8m9tcH30ENy38S2xSILfVKKpmceGu3_qqGmqgvnhV58N01DLdeV2"
    chat_url = f"https://www.douyin.com/douyin-im/chat?uid={target_uid}"
    page.goto(chat_url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(4000)

    if detect_rate_limit(page):
        return False, "检测到验证码/操作频繁"
    # 定位输入框
    try:
        input_box = page.locator('div[contenteditable="true"]').first
        input_box.wait_for(timeout=15000)
    except Exception:
        return False, "找不到聊天输入框"
    if dry_run:
        return True, "测试成功"
    input_box.click()
    page.keyboard.type(msg_text, delay=120)
    page.keyboard.press("Enter")
    time.sleep(3)
    return True, "消息发送成功"
