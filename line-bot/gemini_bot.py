import os
import google.generativeai as genai
import settings

class ChatBot:
    def __init__(self, model_name='gemini-1.5-flash', system_instruction="如果對話內容是中文，使用繁體中文回應。", temperature=1):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.model_name = model_name
        self.system_instruction = system_instruction
        settings.generation_config['temperature'] = temperature
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name, safety_settings=settings.safety_settings, system_instruction=self.system_instruction, generation_config=settings.generation_config)
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message, prefix = 'mode:chatbot\n'):
        resp = self.chat.send_message(message)
        return prefix + resp.text

    def greet(self):
        return 'change mode to Chatbot\n\n' + self.send_message('你好')

class TransBot(ChatBot):
    def __init__(self, model_name='gemini-1.5-flash', system_instruction="你是語言翻譯專家，把對話內容，英文翻成繁體中文，中文翻成英文。直接提供翻譯，不再進行對話。", temperature=0.3):
        super().__init__(model_name, system_instruction, temperature)

    def send_message(self, message, prefix = 'mode:translator\n'):
        return super().send_message("翻譯以下內容\n\n" + message, prefix)

    def greet(self):
        return 'change mode to Translator\n\n' + self.send_message('I can help to translate English and Chinese')

class TeachBot(ChatBot):
    def __init__(self, model_name='gemini-1.5-flash', system_instruction="你是一個教導外國人英文的英文教師，可以在對話一開始詢問一些基本資訊(name,age)，根據基本資訊尋找話題來做英文對話。如果對話中，有使用錯誤的語法或時態，或是有拼錯的字，都可以在對話中指正。", temperature=0.7):
        super().__init__(model_name, system_instruction, temperature)

    def send_message(self, message, prefix = 'mode:teacher\n'):
        return super().send_message(message, prefix)

    def greet(self):
        return 'change mode to English Teacher\n\n' + self.send_message('Hello')

if __name__ == "__main__":
    bot = ChatBot()
    print(bot.greet())
    resp = bot.send_message("你是?")
    print(resp)

    bot = TransBot()
    print(bot.greet())
    resp = bot.send_message("你好")
    print(resp)

    bot = TeachBot()
    print(bot.greet())
    resp = bot.send_message("你好")
    print(resp)

