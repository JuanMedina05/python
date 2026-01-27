import os
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

OLLAMA_BASE_URL = "https://jarvis.ieshlanz.es"  
llm = ChatOllama(model="qwen3:14b", base_url=OLLAMA_BASE_URL, temperature=0.5)

res = llm.invoke([
    SystemMessage(content="Hablame como si fueras Juan Cuesta Aqui no hay quien viva."),
    HumanMessage(content="Explicame la crisis economica que está pasando en Japón por los tipos de intereses"),
])

print(res.content)