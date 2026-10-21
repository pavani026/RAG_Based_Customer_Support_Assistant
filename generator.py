import os

from openai import OpenAI
from langsmith.wrappers import wrap_openai

# wrap_openai makes every LLM call show up as a trace in LangSmith
# (only active when LANGSMITH_TRACING=true and LANGSMITH_API_KEY are set)
client = wrap_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))  # set as env variable!


def generate_answer(query, context):
    try:
        prompt = f"""
You are a customer support assistant.

Context:
{context}

Question:
{query}

Answer clearly:
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content

    except Exception as e:
        print("LLM Error:", e)
        return None
