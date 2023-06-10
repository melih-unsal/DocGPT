from src.models import ChatGPT as Model
from src.models import KeywordGPT

import fire

def main(question, pdf="/home/melih/Downloads/Introduction to User Research_Course_Book.pdf"):
    model = Model(pdf_path= pdf)
    answer = model.answer(question)
    print("-"*100)
    print("Question:",question)
    print("Answer:"+answer)

def keywords(question):
    model = KeywordGPT()
    keywords = model.getKeywords(question)
    print(keywords)
    print("-"*100)
    keywords = keywords[1:-1].split(",")
    for key in keywords:
        print(key.strip())


if __name__ == "__main__":
    fire.Fire(main)