from inference import get_response
import gradio as gr

def respond(user_query, history):
    result = get_response(user_query)
    return result['response']

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    msg.submit(respond, [msg, chatbot], [chatbot])

demo.launch()