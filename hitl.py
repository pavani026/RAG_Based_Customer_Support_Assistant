def human_fallback(query):
    print("\nEscalating to human support...")
    print("User Query:", query)
    answer = input("Enter human response: ")
    return answer
