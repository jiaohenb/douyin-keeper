import time
from ..guard import detect_rate_limit

def send_exist_chat_message(
    nickname: str,
    msg_text: str,
    page,
    context,
    dry_run: bool = False,
) -> tuple[bool, str]:
    # 打开抖音IM主页
    page.goto("https://www.douyin.com/douyin-im", wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(8000)

    # 检测是否掉线
    if "passport" in page.url.lower() or "login" in page.url.lower():
        return False, "Cookie失效，需要重新抓取www.douyin.com的cookie"

    # 定位顶部搜索框，搜索好友昵称
    try:
        search_input = page.locator('input[placeholder="搜索会话"]').first
        search_input.wait_for(timeout=15000)
    except Exception:
        return False, "找不到IM搜索框"

    search_input.click()
    search_input.fill(nickname)
    page.wait_for_timeout(2500)

    # 点击搜索出来的会话条目
    try:
        session_item = page.locator("div.session-item").first
        session_item.wait_for(timeout=12000)
        session_item.click()
    except Exception:
        return False, f"搜索不到好友【{nickname}】的会话"

    page.wait_for_timeout(6000)
    if detect_rate_limit(page):
        return False, "检测到验证码/操作频繁限制"

    # 新版抖音聊天输入框，适配最新页面结构
    try:
        input_box = page.locator('div[role="textbox"]').first
        input_box.wait_for(timeout=20000)
    except Exception:
        return False, "找不到聊天输入框"

    if dry_run:
        return True, "测试定位成功"

    input_box.click()
    page.keyboard.type(msg_text, delay=150)
    page.keyboard.press("Enter")
    time.sleep(3)
    return True, "消息发送成功"
