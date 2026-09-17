from llm import qwen
from tools import calculator, weather, memory
def agent(question):
    text = question.lower()
 
    if text.startswith("calculate "):
        answer = calculator(question[10:])
    elif "weather" in text:
        city = question.lower().rsplit(" in ", 1)[-1].strip(" ?.")
        answer = weather(city)
    else:
        history = "\n".join(memory[-4:])
        prompt = f"Conversation:\n{history}\nUser: {question}\nAssistant:"
        answer = qwen.invoke(prompt)
 
    memory.append(f"User: {question}")
    memory.append(f"Assistant: {answer}")
    
    return answer