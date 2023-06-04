# ExamGPT
Welcome to the ExamGPT repository. This project leverages the powerful language model GPT-3.5, created by OpenAI, to generate accurate and relevant answers based on the content of PDF documents.

## Overview
The primary purpose of this project is to parse and understand PDF documents, and to generate precise answers for questions based on those documents. The mechanism involves dividing the document into smaller, manageable segments, pinpointing the relevant segment(s) for a given question, and generating a comprehensive answer using GPT-3.5.

## How it Works
The ExamGPT process flow consists of two main stages:

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
git clone https://github.com/yourusername/ExamGPT.git
cd ExamGPT
pip3 install -r requirements.txt
```
## Usage
After successfully installing, you can run ExamGPT by following these steps:

Place your PDF document in the designated directory.

Run the segment_pdf.py script to segment the PDF.

Use main.py to generate answers to your questions based on the segmented document.

```
python3 main.py --document_path [segmented_pdf] --question "Your question here"
```
You should see the generated answer printed on your console.

## Contribution
This project is open to contributions! Feel free to create pull requests for bug fixes, improvements, or new features. For larger changes, please open an issue first to discuss what you'd like to change.

## License
This project is under the MIT License.

## Disclaimer
This tool should not be used to encourage academic dishonesty or the violation of any institutional rules regarding exams. It is primarily designed as an aid for study and research. Use responsibly.