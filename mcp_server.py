"""MCP server exposing the RAG Customer Support Assistant as tools.

Test with the MCP Inspector (needs Node.js):
    mcp dev mcp_server.py
"""
import os
from pathlib import Path

# retrieval.py loads the "db" folder by relative path, so always run from the repo folder
os.chdir(Path(__file__).parent)

from mcp.server.fastmcp import FastMCP

from retrieval import retrieve_docs
from generator import generate_answer

mcp = FastMCP("rag-customer-support")


@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """Search the customer support knowledge base (FAQs, policies, product info)
    and return the most relevant passage. Returns a fallback message when nothing
    relevant is found, so the caller can escalate to a human."""
    result = retrieve_docs(query)
    if result is None:
        return "No relevant answer found in the knowledge base. Escalate to a human agent."
    return result


@mcp.tool()
def ask_support_assistant(question: str) -> str:
    """Answer a customer question: retrieve the relevant knowledge-base passage,
    then generate a grounded answer with GPT-4o-mini. Needs OPENAI_API_KEY."""
    context = retrieve_docs(question)
    if context is None:
        return "No relevant answer found in the knowledge base. Escalate to a human agent."
    answer = generate_answer(question, context)
    return answer or "The language model call failed. Escalate to a human agent."


if __name__ == "__main__":
    mcp.run()
