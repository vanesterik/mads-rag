from typing import List

import httpx


def generate_response(prompt: str, documents: List[str]) -> str:
    context = "\n".join(documents)
    full_prompt = parse_template(prompt, context)
    response = httpx.post(
        url="http://localhost:11434/api/generate",
        json={
            "model": "gemma3:1b",
            "prompt": full_prompt,
            "stream": False,
        },
        timeout=None,
    )

    return str(response.json().get("response"))


def parse_template(prompt: str, context: str) -> str:
    return f"""
You are a data scientist. 
Answer the following question using the provided context. 
If you can't find the answer, do not pretend you know it, but answer "I don't know".

Question: {prompt.strip()}

Context: 
{context.strip()}

Answer:
"""
