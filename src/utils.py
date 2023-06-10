
from PyPDF2 import PdfReader
import fire
from tqdm import trange
import tiktoken
import nltk

tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")

def toTextList(filepath,chunk_size=256):
    # creating a pdf reader object
    reader = PdfReader(filepath)
    texts = []
    for i in trange(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        sentences = tokenizer.tokenize(text)
        size = 0
        subtext = ""
        for sentence in sentences:
            size += len(encoder.encode(sentence))
            subtext += sentence
            if size > chunk_size:
                texts.append(subtext)
                size = 0
                subtext = ""
        if subtext:
            texts.append(subtext)
    return texts

SYSTEM_PROMPT = """
You will get a book as a document input and and you are supposed to answer questions based on only this document.
"""

GENERATE_KEYWORDS_SYSTEM_PROMPT = """
You are supposed to generate a python list which includes the keywords to answer the question
"""

GENERATE_KEYWORDS_PROMPT ="""

question : What is the purpose of the envisioning phase, which takes place before the technical implementation?

A) To identify the shortcomings and difficulties in design draft

B) To convince all stakeholders of the design

C) To implement technical functions

D) To check whether the design is technically feasible

keywords : 
```
['envisioning phase', 'technical implementation', 'identify the shortcomings and difficulties in design draft', 'convince all stakeholders of the design', 'implement technical functions', 'checking whether the design is technically feasible']
```

question : <{question}>

keywords:

"""

DOC_PROMPT="""
Document : {doc}

Only depending on the document above, answer the question below:

Question: <{question}>
"""

MS_DOC_PROMPT="""
Document : {doc}

Only depending on the document above, select the best option among the choice for the question below:

Question: <{question}>
"""


if __name__ == '__main__':
    fire.Fire(toTextList)