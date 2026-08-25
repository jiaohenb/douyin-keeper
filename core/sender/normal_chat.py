"""通道A：常规已有会话私信发送（适合日常续火花，风控更低）
适用：已经有聊天会话的好友
"""
from __future__ import annotations
import logging
import time
from ..guard import detect_rate_limit
logger = logging.getLogger("douyin-spark")
CHAT_URL = "https://www.douyin.com/douyin-im"
CHAT_ITEM_SELECTOR = 'xpath=//div[contains(@class, "session-item")]'
NAME_SPAN_SELECTOR = 'xpath=.//span[contains(@class, "name-")]'
CHAT_INPUT_SELECTOR = "xpath=//div[contains(@class, 'input-box')]"


def send_exist_chat_message(
    nickname: str,
    msg_text: str,
    page,
    context,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """已有会话私信发送
    """
    page.goto(CHAT_URL, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(6000)
    if "passport" in page.url.lower() or "login" in page.url.lower():
        return False, "抖音网页版跳转到登录页，Cookie失效"
    # 遍历会话列表匹配昵称
    found = False
    items = page.locator(CHAT_ITEM_SELECTOR).all()
    for it in items:
        try:
            span = it.locator(NAME_SPAN_SELECTOR)
            if span.count() == 0:
                continue
            name = span.inner_text().strip()
            if name == nickname:
                it.click(timeout=5000)
                found = True
                break
        except Exception:
            continue
    if not found:
        return False, f"私信列表没有找到已有会话【{nickname}】"
    page.wait_for_timeout(3000)
    if detect_rate_limit(page):
        return False, "检测到「操作频繁/验证码」，停止本轮"
    try:
        page.wait_for_selector(CHAT_INPUT_SELECTOR, timeout=15000)
    except Exception:
        return False, "未找到聊天输入框"
    if dry_run:
        return True, "dry-run 定位会话成功"
    input_box = page.locator(CHAT_INPUT_SELECTOR).first
    input_box.click()
    page.keyboard.type(msg_text, delay=120)
    page.keyboard.press("Enter")
    time.sleep(3)
    return True, "ok"
