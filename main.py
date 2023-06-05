from models import ChatGPT
import fire


agent = ChatGPT()
def answer(question):
    completion = agent(question)
    print("Assistant:",completion)

if __name__ == "__main__":
    fire.Fire()