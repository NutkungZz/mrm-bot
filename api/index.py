from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import os

CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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

def handler(event, context):
    if event['httpMethod'] == 'POST':
        signature = event['headers'].get('x-line-signature', '')
        body = event['body']
        
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid signature')
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
    elif event['httpMethod'] == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps('Hello, World!')
        }

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    handle_message(event)
