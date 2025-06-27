from inference import get_response
import gradio as gr

class ChatbotRAG:
    def __init__(self):
        self.history = []

    def respond(self, user_message):
        self.history.append(("Пользователь", user_message))
        result = get_response(user_message)

        if result['success']:
            answer = result['response']
        else:
            answer = "⚠️ Ошибка: " + result.get('error', 'Неизвестная ошибка')

        self.history.append(("Бот", answer))
        formatted_history = [list(pair) for pair in self.history]

        return formatted_history, formatted_history

chatbot = ChatbotRAG()

with gr.Blocks() as demo:
    chatbot_component = gr.Chatbot(label="Чат-бот по трудовому праву")
    user_input = gr.Textbox(placeholder="Введите ваш вопрос по трудовому праву и нажмите Enter")
    
    user_input.submit(chatbot.respond, inputs=user_input, outputs=[chatbot_component, chatbot_component])

demo.launch()
