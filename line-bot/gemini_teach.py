import os
import google.generativeai as genai
import settings

class TeachBot:
    def __init__(self):
        self.model_name = 'gemini-1.5-flash'
        self.api_key = os.environ.get('GEMINI_API_KEY')
        settings.generation_config['temperature'] = 0.6
        self.system_instruction = "你是一個教導外國人英文的英文教師，可以在對話一開始詢問一些基本資訊，根據基本資訊尋找話題來做英文對話。如果對話中，有使用錯誤的語法，或是有拼錯的字，都可以在對話中指正。"
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name, system_instruction=self.system_instruction, safety_settings=settings.safety_settings, generation_config=settings.generation_config)
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message, prefix = 'mode:teacher\n'):
        resp = self.chat.send_message(message)
        return prefix + resp.text

    def greet(self):
        return 'change mode to English Teacher\n\n' + self.send_message('Hello')

if __name__ == "__main__":
    bot = TeachBot()
    resp = bot.send_message("hello")
    print(resp)

