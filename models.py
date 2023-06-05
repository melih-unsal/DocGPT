import os
from dotenv import load_dotenv
import openai
import utils
import copy

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY


class OpenAIModel:
    def __init__(self, model):
        self.model = model
        self.next_roles = {
            "user":"assistant",
            "assistant":"user"
            }
        self.messages = []

    def getRole(self, messages):
        if len(messages) % 2 == 0:
            return "user"
        return "assistant"

    def get_completion(self,content):
        self.addMessage(content)
        completion = self.get_output()
        self.addMessage(completion)
        return completion
    
    def get_completion_without_history(self,content):
        completion = self.get_output(content)
        return completion


class ChatGPT(OpenAIModel):
    def __init__(self, model = "gpt-3.5-turbo", system_message=utils.SYSTEM_PROMPT,pdf_path=None):
        assert pdf_path, "Please specify a pdf_path"
        assert os.path.exists(pdf_path), "Please specify a valid pdf_path"
        super().__init__(model)
        self.messages = [{"role": "system", "content" :system_message}]
        self.start_messages = copy.deepcopy(self.messages)
        self.pdf_path = pdf_path
        self.constructTexts()

    def constructTexts(self):
        self.texts = utils.toTextList(self.pdf_path)

    def addMessage(self,content):
        role = self.getRole(self.messages)
        message = {"role": role, "content":content}
        self.messages.append(message)
    
    def get_output(self, prompt=None):
        if prompt:
            result = openai.ChatCompletion.create(
                model=self.model,
                messages = self.start_messages.extend([{"role":"user","content":prompt}])
                )
        else:
            result = openai.ChatCompletion.create(
                model=self.model,
                messages = self.messages
            )
        completion = result["choices"][0]["message"]["content"]
        return completion




