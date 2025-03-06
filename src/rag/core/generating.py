from typing import Dict

from openai import Client

from rag.common.config import LLM_MODEL


def generate_answer(client: Client, context: str, query: str) -> Dict[str, str | None]:
    # Define system message with context
    system_message = f"You are a helpful assistant. Here is the context to use to reply to questions: {context}"

    # Make the OpenAI API call with the updated context
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ],
    )
    return {"response": response.choices[0].message.content}
