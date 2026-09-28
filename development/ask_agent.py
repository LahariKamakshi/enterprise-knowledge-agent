from hindsight_client import Hindsight
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Hindsight connection
# -----------------------------

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)


# -----------------------------
# Ask a question
# -----------------------------

question = "Who is responsible for the database deployment in Project Orion?"


print("\nQuestion:")
print(question)


# -----------------------------
# Recall from Hindsight
# -----------------------------

result = client.recall(
    bank_id="enterprise-knowledge",
    query=question
)


# -----------------------------
# Display memory
# -----------------------------

print("\nHindsight Memory:")
print("--------------------------------")

print(result)
