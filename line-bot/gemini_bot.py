import os
from google import genai
from google.genai import types
import settings

class ChatBot:
    def __init__(self, model_name='gemini-2.5-flash', cfg=settings.chatcfg):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.model_name = model_name
        self.system_instruction = cfg['system_instruction']
        gen_cfg = dict(settings.generation_config)
        gen_cfg['temperature'] = cfg['temperature']
        gen_cfg['system_instruction'] = self.system_instruction
        gen_cfg['safety_settings'] = settings.safety_settings

        self.client = genai.Client(api_key=self.api_key)
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(**gen_cfg),
        )

    def send_message(self, message, prefix = 'mode:chatbot\n'):
        resp = self.chat.send_message(message)
        return prefix + resp.text

    def greet(self):
        return 'change mode to Chatbot\n\n' + self.send_message('你好')

class TransBot(ChatBot):
    def __init__(self, model_name='gemini-2.5-flash', cfg=settings.transcfg):
        super().__init__(model_name, cfg)

    def send_message(self, message, prefix = 'mode:translator\n'):
        return super().send_message("翻譯以下內容\n\n" + message, prefix)

    def greet(self):
        return 'change mode to Translator\n\n' + self.send_message('I can help to translate English and Chinese')

class TeachBot(ChatBot):
    def __init__(self, model_name='gemini-2.5-flash', cfg=settings.teachcfg):
        super().__init__(model_name, cfg)

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

