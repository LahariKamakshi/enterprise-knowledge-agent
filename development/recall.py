from hindsight_client import Hindsight
from data import project_orion_data
import os
from dotenv import load_dotenv

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

print("Hindsight connected!")

result = client.recall(
    bank_id="enterprise-knowledge",
    query="What information is contained in the Coding Ninjas email?"
)

print("Recall result:")
print(result)