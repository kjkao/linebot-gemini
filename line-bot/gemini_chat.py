import os
import google.generativeai as genai

class ChatBot:
    def __init__(self):
        self.model_name = 'gemini-1.5-flash'
        self.api_key = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message):
        resp = self.chat.send_message(message)
        return resp.text

if __name__ == "__main__":
    bot = ChatBot()
    resp = bot.send_message("你好")
    print(resp)
    resp = bot.send_message("你知道今天是什麼日子嗎?")
    print(resp)

