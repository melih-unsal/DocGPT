from dotenv import load_dotenv
import os
load_dotenv()
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


class LangchainModel:
    def __init__(self,filepath='/home/melih/Downloads/Introduction to User Research_Course_Book.txt'):
        loader = TextLoader(filepath)
        self.index = VectorstoreIndexCreator().from_loaders([loader])
        self.llm = OpenAI(temperature=0.0)
    
    def answer(self,query):
        answer = self.index.query(query)
        print(answer)
        if "i don't know" in answer.lower():
            answer = self.llm(query)
            answer = "Document-based answer has failed. Question is asked to standard model...\n"+"."*100+"\n" + answer

        return answer

