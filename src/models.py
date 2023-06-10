import os
from dotenv import load_dotenv
import openai
import copy
from src.utils import SYSTEM_PROMPT, DOC_PROMPT, GENERATE_KEYWORDS_SYSTEM_PROMPT, GENERATE_KEYWORDS_PROMPT, MS_DOC_PROMPT, encoder
from src.embeddings import Embeddings
import fire
from tqdm import tqdm

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
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
        while True:
            try:
                completion = self.get_output()     
                self.addMessage(completion)   
            except Exception as e:
                print("API Error during",self.model_name,"processing")
            else:
                break
        return completion
    
    def get_completion_without_history(self,content):
        self.addMessage(content)
        completion = self.get_output()
        self.addMessage(completion)
        return completion


class KeywordGPT(OpenAIModel):
    def __init__(self, model = "gpt-3.5-turbo", system_message=GENERATE_KEYWORDS_SYSTEM_PROMPT):
        super().__init__(model)
        self.messages = [{"role": "system", "content" :system_message}]

    def get_output(self, prompt=None):
        if prompt:
            result = openai.ChatCompletion.create(
                model=self.model,
                messages = self.messages + [{"role":"user","content":prompt}]
                )
        else:
            result = openai.ChatCompletion.create(
                model=self.model,
                messages = self.messages
            )
        completion = result["choices"][0]["message"]["content"]
        return completion
    
    def getKeywords(self,question):
        prompt = GENERATE_KEYWORDS_PROMPT.format(question=question)
        keywords = self.get_output(prompt)
        return keywords[1:-1].split(",")


class ChatGPT(OpenAIModel):
    def __init__(self, model = "gpt-3.5-turbo", system_message=SYSTEM_PROMPT,pdf_path="/home/melih/Downloads/Introduction to User Research_Course_Book.pdf"):
        valid = os.path.exists(pdf_path or "")
        super().__init__(model)
        self.keyword_model = KeywordGPT()
        self.messages = [{"role": "system", "content" :system_message}]
        self.start_messages = copy.deepcopy(self.messages)
        self.pdf_path = pdf_path
        self.embedding_model = Embeddings()
        if valid:
            self.embedding_model.setDocs(self.pdf_path)
        
    def setDocs(self, doc_path):
        self.embedding_model.setDocs(doc_path)

    def answer(self,question):
        keywords = self.keyword_model.getKeywords(question)
        print("keywords are,",keywords)
        documents = []
        for keyword in tqdm(keywords):
            doc = self.embedding_model(keyword,2)
            documents += doc
        if "A)" in question and "B)" in question:
            prompt = MS_DOC_PROMPT.format(question=question, doc=documents)
        else:
            prompt = DOC_PROMPT.format(question=question, doc=documents)
        print("prompt:",prompt)
        print("len(encoder.encode(prompt)):",len(encoder.encode(prompt)))
        return self.get_output(prompt)

    def addMessage(self,content):
        role = self.getRole(self.messages)
        message = {"role": role, "content":content}
        self.messages.append(message)
    
    def get_output(self, prompt=None):
        while True:
            try:
                result = openai.ChatCompletion.create(
                    model=self.model,
                    messages = self.start_messages + [{"role":"user","content":prompt}]
                )  
            except Exception as e:
                print("API Error during",self.model_name,"processing")
            else:
                break
        completion = result["choices"][0]["message"]["content"]
        return completion


if __name__ == "__main__":
    fire.Fire(KeywordGPT)

