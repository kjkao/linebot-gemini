from datetime import datetime, timedelta

class AutoReplyManager:
    def __init__(self, timeout=8):
        self.data = []
        self.timeout = timeout

    def add_message(self, key, msg, emojis=None):
        current_time = datetime.now()
        self.data.append({'key': key, 'msg': msg, 'emojis': emojis, 'time': current_time})
        self._cleanup()

    def update_message(self, key, msg, emojis=None):
        current_time = datetime.now()
        for item in self.data:
            if item['key'] == key:
                item['msg'] = msg
                item['emojis'] = emojis
                item['time'] = current_time
        self._cleanup()

    def delete_message(self, key):
        self.data = [item for item in self.data if item['key'] != key]

    def get_message(self, key):
        self._cleanup()
        for item in self.data:
            if item['key'] == key:
                return item['msg'], item['emojis']
        return None

    def list_messages(self):
        self._cleanup()
        return self.data

    def _cleanup(self):
        current_time = datetime.now()
        self.data = [item for item in self.data if current_time - item['time'] <= timedelta(hours=self.timeout)]

if __name__ == "__main__":
    manager = AutoReplyManager()
    manager.add_message('key1', 'Hello, World!')
    manager.add_message('key2', '這是一段中文訊息')

    print(manager.get_message('key1'))
    print(manager.get_message('key2'))

    import time
    time.sleep(5)
    manager.add_message('key3', '新消息')
    print(manager.get_message('key1'))
    print(manager.get_message('key3'))
    print(manager.list_messages())
