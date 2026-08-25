import os
import sys
sys.path.append(os.path.dirname(__file__))

from core.sender.creator_channel import send_first_message

if __name__ == "__main__":
    #读取仓库Secrets里面保存好的配置
    COOKIES = os.getenv("COOKIES")
    TARGET_NAME = os.getenv("TARGET_NAME")
    MSG = os.getenv("MSG")

    if not all([COOKIES, TARGET_NAME, MSG]):
        print("❌ 缺失环境变量！检查Secrets: COOKIES、TARGET_NAME、MSG")
        sys.exit(1)

    friend_list = [x.strip() for x in TARGET_NAME.split(",")]
    print(f"✅待发送好友：{friend_list}")
    print(f"✅发送消息：{MSG}")

    for nick in friend_list:
        print(f"\n👉开始给【{nick}】发送消息")
        success, info = send_first_message({"nickname": nick}, MSG)
        print(f"结果：{success} - {info}")

    print("\n🎉全部任务执行完毕，程序正常退出！")

