# DocGPT
Welcome to the DocGPT repository. This project leverages the powerful language model GPT-3.5, created by OpenAI, to generate accurate and relevant answers based on the content of PDF documents.

## Overview
The primary purpose of this project is to parse and understand PDF documents, and to generate precise answers for questions based on those documents. The mechanism involves dividing the document into smaller, manageable segments, pinpointing the relevant segment(s) for a given question, and generating a comprehensive answer using GPT-3.5.

## How it Works
The DocGPT process flow consists of two main stages:

### Document Segmentation: 
The input PDF document is divided into small segments. These are manageable, searchable sections that can be easily analysed for relevant content.

### Question Answering: 
The segments are searched for the best parts that can provide a relevant answer to the input question. Once the segments are selected, GPT-3.5 is used to generate the answer based on the content of those segments.

This approach ensures that the model generates accurate and contextually relevant answers.

## Installation
Requirements
Python 3.8+
Pip3
Clone the repository and install the necessary dependencies by running the following commands:
```
git clone https://github.com/yourusername/DocGPT.git
cd DocGPT
pip3 install -r requirements.txt
```
## Usage
After successfully installing, you can run DocGPT by following these steps:

Place your PDF document in the designated directory.

You will then need to set the environment variable in the terminal.

```
export OPENAI_API_KEY="..."
```

Alternatively, you could do this from inside the Jupyter notebook (or Python script):
```
import os
os.environ["OPENAI_API_KEY"] = "..."
```

Use app.py to start the gradio application. You can either put the pdf file path as an argument or after you run the application, you can directly upload the pdf file.

```
python app.py --pdf <DOCUMENT_PATH>(Optional) --port <port number> (Optional)
```
Then, you should see the gradio application on localhost:8000 (if you don't provide a port)

## Contribution
This project is open to contributions! Feel free to create pull requests for bug fixes, improvements, or new features. For larger changes, please open an issue first to discuss what you'd like to change.

## License
This project is under the MIT License.

## Disclaimer
This tool should not be used to encourage academic dishonesty or the violation of any institutional rules regarding exams. It is primarily designed as an aid for study and research. Use responsibly.
