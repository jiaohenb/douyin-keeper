import os
import json
import sys
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
from playwright.sync_api import sync_playwright
from core.sender.creator_channel import _do_send

if __name__ == "__main__":
    COOKIES_RAW = os.getenv("COOKIES")
    TARGET_NAME = os.getenv("TARGET_NAME")
    MSG = os.getenv("MSG")

    if not all([COOKIES_RAW, TARGET_NAME, MSG]):
        print("❌ 缺失环境变量！检查Secrets: COOKIES、TARGET_NAME、MSG")
        sys.exit(1)

    # 自动创建data文件夹（兜底）
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)

    friend_list = [x.strip() for x in TARGET_NAME.split(",")]
    print(f"✅待发送好友：{friend_list}")
    print(f"✅发送消息：{MSG}")

    # 字符串cookie转playwright标准cookie数组
    cookie_list = []
    for item in COOKIES_RAW.split(";"):
        item = item.strip()
        if "=" not in item:
            continue
        k, v = item.split("=", 1)
        cookie_list.append({
            "name": k.strip(),
            "value": v.strip(),
            "domain": ".douyin.com",
            "path": "/"
        })

    for nick in friend_list:
        print(f"\n👉开始给【{nick}】发送消息")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox",
                      "--disable-dev-shm-usage", "--disable-gpu"],
            )
            # 新建上下文，不读取state.json，直接注入cookie
            context = browser.new_context(
                viewport={"width": 1366, "height": 900},
                locale="zh-CN",
            )
            context.add_cookies(cookie_list)
            page = context.new_page()
            success, info = _do_send(page, context, nick, MSG, dry_run=False, max_scrolls=80)
            browser.close()
        print(f"结果：{success} - {info}")

    print("\n🎉全部任务执行完毕，程序正常退出！")
