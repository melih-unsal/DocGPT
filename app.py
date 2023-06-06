import gradio as gr
import time
import fire
from src.models import ChatGPT as Model

model = Model()

def uploadFile(f):
    filepath = f.name
    model.setDocs(filepath)

def main(port=8000,pdf=None):
    
    with gr.Blocks() as demo:
        gr.Markdown(
            """
        # PdfReaderGPT
        Upload your pdf and ask questions
        """
        )

        file_output = gr.File()
        upload_button=gr.UploadButton(file_types=[".pdf"])
        upload_button.upload(uploadFile, upload_button, file_output)

        if pdf:
            model.setDocs(pdf)

        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")

        def user(user_message, history):
            return "", history + [[user_message, None]]

        def bot(chat_history):
            message = chat_history[-1][0]
            bot_message = model.answer(message)
            chat_history[-1][1] = ""
            for character in bot_message:
                chat_history[-1][1] += character
                time.sleep(0.01)
                yield chat_history

        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
    demo.queue()
    demo.launch(server_name="0.0.0.0", server_port=port)

if __name__ == "__main__":
    fire.Fire(main)