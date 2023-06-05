
from PyPDF2 import PdfReader
import fire
from tqdm import trange
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")

def toTextList(filepath,chunk_size=2000, per_page=True):
    # creating a pdf reader object
    reader = PdfReader(filepath)
    text = ""
    texts = []
    for i in trange(len(reader.pages)):
        page = reader.pages[i]
        text += page.extract_text()
        size = len(encoder.encode(text))
        if size > chunk_size or per_page:
            texts.append(text)
            text = ""
    if text:
        texts.append(text)
    return texts

SYSTEM_PROMPT = """
You will get a book as a document input and and you are supposed to answer questions based on only this document.
"""

DOC_PROMPT="""
Please answer the question <{question}> only using the document below:

<{doc}>
"""

if __name__ == '__main__':
    fire.Fire(toTextList)