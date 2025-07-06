class ChatMemory:
    def __init__(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get(self):
        return self.messages