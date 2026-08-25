import time
from playwright.sync_api import Page
from ..base import BaseSender


class NormalChatSender(BaseSender):
    def send(self, page: Page, nickname: str, content: str) -> tuple[bool, str]:
        """
        nickname: 川平
        content: 要发送的续火花消息
        """
        try:
            # 打开抖音IM主页
            page.goto("https://www.douyin.com/chat", timeout=60000)
            page.wait_for_timeout(3000)

            # 左侧搜索框，搜索好友名字
            search_input = page.locator('input[placeholder="搜索"]')
            search_input.wait_for(timeout=15000)
            search_input.fill(nickname)
            page.wait_for_timeout(2000)

            # 点击匹配出来的好友会话
            friend_item = page.locator(f"div:has-text('{nickname}')").first
            friend_item.wait_for(timeout=15000)
            friend_item.click()
            page.wait_for_timeout(3000)

            # 定位底部消息输入框
            msg_input = page.locator('input[placeholder="发送消息"]')
            msg_input.wait_for(timeout=20000)
            msg_input.fill(content)
            page.wait_for_timeout(1000)
            msg_input.press("Enter")

            time.sleep(2)
            return True, "发送成功"
        except Exception as e:
            return False, f"失败：{str(e)}"
