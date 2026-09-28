import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

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
# Start agent
# -----------------------------

print("\n========================================")
print("   ENTERPRISE KNOWLEDGE AGENT")
print("========================================")
print("Ask questions about your enterprise data.")
print("Type 'exit' to stop.\n")


while True:

    # -----------------------------
    # Get user question
    # -----------------------------

    question = input("Ask a question: ").strip()


    # -----------------------------
    # Exit
    # -----------------------------

    if question.lower() == "exit":
        print("\nAgent stopped.")
        break


    if not question:
        continue


    # -----------------------------
    # Recall from Hindsight
    # -----------------------------

    result = hindsight_client.recall(
        bank_id="enterprise-knowledge",
        query=question
    )


    # -----------------------------
    # Extract memories
    # -----------------------------

    memories = []

    for item in result.results:
        memories.append(item.text)


    context = "\n".join(memories)


    # -----------------------------
    # Ask Groq
    # -----------------------------

    prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the
retrieved enterprise memories below.

Do not invent information.

If the information is not available,
say that it is not available in the
enterprise memory.

Keep the answer concise and clear.

Retrieved enterprise memories:
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
    # Display answer
    # -----------------------------

    answer = response.choices[0].message.content


    print("\nAgent:")
    print(answer)
    print()
