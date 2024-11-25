import requests
import time

# サーバーのURL
SERVER_URL = "https://a15ba53f-9b9f-4295-8ea5-a620e489fead-00-nm2f5z1y10pa.pike.replit.dev/send"

for i in range(1, 26):
    # 送信するメッセージ
    message = f"{i},{i*10}"
    
    # POSTリクエストを送信
    response = requests.post(SERVER_URL, data={"message": message})
    
    # サーバーからの応答を表示
    print("Server response:", response.text)
    
    time.sleep(1)
    
