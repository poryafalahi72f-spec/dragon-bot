import os
import time
import json
import urllib.request

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN تنظیم نشده است")

API = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(chat_id, text):
    data = json.dumps({
        "chat_id": chat_id,
        "text": text
    }).encode()

    req = urllib.request.Request(
        API + "sendMessage",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    urllib.request.urlopen(req)

def main():
    offset = 0
    print("DragonBot is running!")

    while True:
        try:
            url = API + f"getUpdates?offset={offset}&timeout=30"
            response = urllib.request.urlopen(url, timeout=40)
            updates = json.loads(response.read())

            for update in updates.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")

                if not chat_id:
                    continue

                if text == "/start":
                    send_message(chat_id, "سلام! 🐉 من DragonBot هستم.")
                elif text == "/ping":
                    send_message(chat_id, "من آنلاینم! ❤️")
                elif text == "/help":
                    send_message(chat_id, "دستورات من:\n/start\n/ping\n/help")

        except Exception as error:
            print(error)
            time.sleep(5)

if name == "main":
    main()
