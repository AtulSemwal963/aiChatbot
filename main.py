# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate

# template= """
# You are an intelligent and friendly AI assistant. Respond clearly, naturally, and without grammatical errors.

# Here is the conversation history:
# {context}

# Question: {question}

# Answer:
# """

# model= OllamaLLM(model="llama3.2:1b")
# prompt= ChatPromptTemplate.from_template(template)
# chain = prompt | model

# def handle_conversation():
#    context = ""
#    print("Welcome to theh AI ChatBot ! Type 'exit' to quit.")
#    while True:
#       user_input=input("You: ")
#       if user_input.lower() == "exit":
#          break 

#       result=chain.invoke({"context":"","question":user_input})
#       print("Bot: ",result)
#       context += f"\nUser: {user_input}\nAI: {result}"
      

# if __name__ == "__main__":
#  handle_conversation()

#  source CHATBOT/Scripts/activate
#uvicorn CHATBOT.main:app --host 127.0.0.1 --port 8000 --reload
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize the Llama model and prompt template
template = """
You are an intelligent and friendly AI assistant. Respond clearly, naturally, and without grammatical errors.

Here is the conversation history:
{context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.2:1b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Initialize FastAPI app
app = FastAPI()

# Store conversation history in memory (for simplicity)
conversation_context = ""

# Define request and response schema using Pydantic
class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    bot_response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    global conversation_context
    user_input = request.user_input

    # Invoke the chatbot chain
    result = chain.invoke({"context": conversation_context, "question": user_input})
    
    # Update the context
    conversation_context += f"User: {user_input}\nAI: {result}\n"

    return ChatResponse(bot_response=result)
