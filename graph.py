from langgraph.graph import StateGraph


def process_node(state):
    query = state["query"]

    # 1. Retrieve relevant text from the ChromaDB knowledge base
    context = state["retriever"](query)
    if not context:
        state["escalate"] = True
        return state

    # 2. Generate a grounded answer with the LLM (generator.py -> GPT-4o-mini)
    answer = state["generator"](query, context)
    if not answer:
        # LLM failed -> escalate to a human
        state["escalate"] = True
        return state

    state["answer"] = answer
    state["escalate"] = False
    return state


def output_node(state):
    # Human-in-the-loop: if nothing reliable was found, hand over to a human
    if state["escalate"]:
        state["answer"] = state["hitl"](state["query"])
    return state


def build_graph():
    graph = StateGraph(dict)
    graph.add_node("process", process_node)
    graph.add_node("output", output_node)
    graph.set_entry_point("process")
    graph.add_edge("process", "output")
    return graph.compile()
