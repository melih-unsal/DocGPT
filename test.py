from src.models import ChatGPT as Model
import fire

def main(pdf, question):
    model = Model(pdf_path= pdf)
    answer = model.answer(question)
    print("-"*100)
    print("Question:",question)
    print("Answer:"+answer)

if __name__ == "__main__":
    fire.Fire(main)