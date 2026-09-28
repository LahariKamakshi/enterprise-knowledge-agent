from hindsight_client import Hindsight
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# Hindsight connection
# -----------------------------

hindsight_client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)


# -----------------------------
# Groq connection
# -----------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# User question
# -----------------------------

question = "Who is responsible for the database deployment in Project Orion?"


print("\nUser Question:")
print(question)


# -----------------------------
# Recall relevant memories
# -----------------------------

result = hindsight_client.recall(
    bank_id="enterprise-knowledge",
    query=question
)


# -----------------------------
# Extract memory text
# -----------------------------

memories = []

for item in result.results:

    memories.append(item.text)


context = "\n".join(memories)


# -----------------------------
# Ask Groq to answer
# -----------------------------

prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the information
provided in the retrieved memories.

Do not invent information.

If the answer is not present in the memories,
say that the information is not available.

Give a concise and direct answer.

Retrieved memories:
{context}

User question:
{question}
"""


response = groq_client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)


# -----------------------------
# Final answer
# -----------------------------

answer = response.choices[0].message.content


print("\nAgent Answer:")
print("--------------------------------")
print(answer)
