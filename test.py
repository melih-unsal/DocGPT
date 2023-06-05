from src.models import ChatGPT as Model

pdf_path = "/home/melih/Downloads/Introduction to User Research_Course_Book.pdf"
question = """
If a little trust in "User Research" has already been built up in the development team and in
the company, then you can use so-called "slides" as a medium for the "Research Report".
Briefly describe the five contents that should be presented on the "slides".
Also describe one advantage and one disadvantage of this method.
"""

model = Model(pdf_path= pdf_path)
answer = model.answer(question)
print("-"*100)
print("Question:",question)
print("Answer:"+answer)