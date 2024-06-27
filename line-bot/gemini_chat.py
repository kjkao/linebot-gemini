import os
import google.generativeai as genai
import settings

class ChatBot:
    def __init__(self):
        self.model_name = 'gemini-1.5-flash'
        self.api_key = os.environ.get('GEMINI_API_KEY')
        settings.generation_config['temperature'] = 1
        self.system_instruction="如果對話內容是中文，使用繁體中文回應。"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name, safety_settings=settings.safety_settings, system_instruction=self.system_instruction, generation_config=settings.generation_config)
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message, prefix = 'mode:chatbot\n'):
        resp = self.chat.send_message(message)
        return prefix + resp.text

    def greet(self):
        return 'change mode to Chatbot\n\n' + self.send_message('你好')

if __name__ == "__main__":
    bot = ChatBot()
    resp = bot.send_message("你好")
    print(resp)

