import os
import google.generativeai as genai
import settings

class TransBot:
    def __init__(self):
        self.model_name = 'gemini-1.5-flash'
        self.api_key = os.environ.get('GEMINI_API_KEY')
        settings.generation_config['temperature'] = 0.3
        self.system_instruction="你是語言翻譯專家，把對話內容，英文翻成繁體中文，中文翻成英文。直接提供翻譯，不再進行對話。"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name, system_instruction=self.system_instruction, safety_settings=settings.safety_settings, generation_config=settings.generation_config)
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message, prefix = 'mode:translator\n'):
        resp = self.chat.send_message("翻譯以下內容\n\n" + message)
        return prefix + resp.text

    def greet(self):
        return 'change mode to Translator'

if __name__ == "__main__":
    bot = TransBot()
    resp = bot.send_message("你好")
    print(resp)

