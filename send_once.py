import os
import json
import sys
from pathlib import Path
sys.path.append(os.path.dirname(__file__))

from core.sender.creator_channel import _do_send
from core.browser import open_browser

if __name__ == "__main__":
    COOKIES_RAW = os.getenv("COOKIES")
    TARGET_NAME = os.getenv("TARGET_NAME")
    MSG = os.getenv("MSG")

    if not all([COOKIES_RAW, TARGET_NAME, MSG]):
        print("❌ 缺失环境变量！检查Secrets: COOKIES、TARGET_NAME、MSG")
        sys.exit(1)

    # 自动创建data目录，避免找不到文件夹
    data_dir = Path("./data")
    data_dir.mkdir(exist_ok=True)

    friend_list = [x.strip() for x in TARGET_NAME.split(",")]
    print(f"✅待发送好友：{friend_list}")
    print(f"✅发送消息：{MSG}")

    # 把cookie字符串转成playwright可用的cookie数组
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
        with open_browser(viewport={"width": 1366, "height": 900}, locale="zh-CN") as (p, browser, context, page):
            # 手动注入cookie，不再读取state.json
            context.add_cookies(cookie_list)
            success, info = _do_send(page, context, nick, MSG, dry_run=False, max_scrolls=80)
        print(f"结果：{success} - {info}")

    print("\n🎉全部任务执行完毕，程序正常退出！")
