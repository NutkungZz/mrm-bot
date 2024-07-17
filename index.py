from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_text = "ขอโทษค่ะ ฉันไม่เข้าใจคำสั่งนี้"

    if text == "สถานะ server":
        reply_text = "Server MRM กำลังทำงานปกติ"
    elif text == "รายงานปัญหา":
        reply_text = "กรุณาแจ้งรายละเอียดปัญหาที่พบ"
    elif text.startswith("ปัญหา:"):
        print(f"ได้รับรายงานปัญหา: {text[6:]}")
        reply_text = "ขอบคุณสำหรับการรายงานปัญหา ทีมงานจะรีบดำเนินการแก้ไขโดยเร็วที่สุด"
    elif text == "ความครบถ้วนของข้อมูล":
        completeness = 95  # ตัวอย่างค่า
        reply_text = f"ความครบถ้วนของข้อมูล: {completeness}%"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text))

@app.route('/')
def hello():
    return 'Hello, World!'

# สำหรับ Vercel
from http.server import BaseHTTPRequestHandler

def handler(event, context):
    return app(event, context)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, World!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = app({'body': body, 'headers': self.headers}, None)
        self.wfile.write(response['body'].encode())

if __name__ == "__main__":
    app.run()
