from react_agent import run_react_agent

print("\n========== QUERY 1 ==========\n")

answer_1 = run_react_agent(
    "What's the current temperature on Crude Distillation Unit 1 (CDU-1)? Is it within normal range?"
)

print("\nFinal Response:")
print(answer_1)

print("\n========== QUERY 2 ==========\n")

answer_2 = run_react_agent(
    "FCC-2's cracking efficiency seems to have dropped overnight. Investigate and tell me what's going on and what we should do."
)

print("\nFinal Response:")
print(answer_2)

while True:

    query = input("\nEnter your question (or 'quit' to exit): ")
    if query.lower() == "quit":
        break

    answer = run_react_agent(query)

    print("\nFinal Response:")
    print(answer)