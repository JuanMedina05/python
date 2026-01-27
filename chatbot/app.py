import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

OLLAMA_BASE_URL="https://jarvis.ieshlanz.es"
llm = ChatOllama(base_url=OLLAMA_BASE_URL, model="qwen3:14b", temperature=0.7)


prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{pregunta}"),
])

chain = prompt | llm

def chat():
    print("Iniciando chat con ALF. Escribe 'salir' para terminar.")

    messages = [
        SystemMessage(content="Hablame como si fueras ALF, el extraterrestre de Melmac"),
    ]

    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break


        response = chain.invoke({
    "pregunta": user_input,
    "messages": messages
})


        #actualizar historial
        messages.append(HumanMessage(content=user_input))
        messages.append(AIMessage(content=response.content))

        print(f"ALF: {response.content}")
    


if __name__ == "__main__":
    chat()