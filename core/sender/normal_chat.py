import time
from ..guard import detect_rate_limit

def send_exist_chat_message(
    nickname: str,
    msg_text: str,
    page,
    context,
    dry_run: bool = False,
) -> tuple[bool, str]:
    # 直接使用你这个可用的弹窗私聊地址
    chat_url = "https://douyin.com/chat?isPopup=1"
    page.goto(chat_url, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(10000)

    # 判断cookie失效跳登录
    if "passport" in page.url.lower() or "login" in page.url.lower():
        return False, "Cookie失效，重新抓取www.douyin.com的cookie"

    if detect_rate_limit(page):
        return False, "检测到验证码/操作频繁限制"

    # 定位底部【发送消息】输入框
    try:
        input_box = page.locator('input[placeholder="发送消息"]').first
        input_box.wait_for(timeout=20000)
    except Exception:
        return False, "找不到发送消息输入框"

    if dry_run:
        return True, "定位成功"

    input_box.click()
    input_box.fill(msg_text)
    page.keyboard.press("Enter")
    time.sleep(3)
    return True, "消息发送成功"
