import re
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser
from files_processing.models import model, vector_store
from query.answer_schema import Topic

def get_response(user_query):
    parser = PydanticOutputParser(pydantic_object=Topic)

    def clean_response(text):
        return re.sub(r"``````", "", text, flags=re.IGNORECASE).strip()

    def parse_topic_articles(llm_response):
        cleaned_text = clean_response(llm_response)
        try:
            return parser.parse(cleaned_text)
        except Exception as e:
            return None
        
    def format_topic(topic_obj):
        if not topic_obj:
            return "⚠️ Не удалось обработать ответ системы"
        
        result = []
        result.append(f"📚 Тема: {topic_obj.topic}")
        result.append(f"📝 Краткое описание:\n{topic_obj.description.replace('\\n', '\n')}\n")
        result.append("📋 Статьи:")

        if not topic_obj.laws:
            result.append("⚠️ Не найдено релевантных статей")
        else:
            for i, article in enumerate(topic_obj.laws, 1):
                result.append(f"\n{i}. Статья:")
                result.append(article.article.replace("\\n", "\n").replace('\n\n', '\n'))
                result.append("   💡 Объяснение:")
                result.append(article.explanation.replace("\\n", "\n").replace('\n\n', '\n'))
                result.append("   📑 Подпункты:")
                result.append(article.subparagraphs.replace("\\n", "\n").replace('\n\n', '\n'))
                
        return "\n".join(result)
    
    try:
        relevant_docs = vector_store.similarity_search(user_query, k=3)
        context = "\n\n".join(doc.page_content for doc in relevant_docs)

        system_prompt = f"""
Ты — эксперт по трудовому праву России. 
Вот релевантные документы:

{context}

Ответь на запрос строго в формате JSON:

{parser.get_format_instructions()}

Если информации нет, верни пустой список laws.
"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]

        response = model.invoke(messages)
        topic_result = parse_topic_articles(response.content)
        formatted_output = format_topic(topic_result)

        return {
            'succes': True,
            'response': formatted_output,
            'raw_data': topic_result
        }
    except Exception as e:
        return {
            'succes': False,
            'error': f"Ошиибка обработки запроса: {str(e)}",
            'response': "⚠️ Произошла ошибка при обработке вашего запроса"
        }