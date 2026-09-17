from tools import calculator, weather, memory
from agent import agent
from speech import text_to_audio, SARVAM_API_KEY

response = agent("Hello, how are you?")
print(response)

audio_file = text_to_audio(response, SARVAM_API_KEY)

print(f"Audio response saved to: {audio_file}")



print(agent("What is an AI agent?"))

print(agent("Calculate 25000 * 0.08"))
print()

print(agent("What is the weather in Bhopal?"))
print()

print(agent("My name is Medha"))
print()

print(agent("What is my name?"))
print()

print("Stored memory:")

for message in memory:
    print(message)

# memory.clear()
while True:
    question = input("You: ")
    
    if question.lower() == "quit":
        break
    
    print("Assistant: " + agent(question))
    