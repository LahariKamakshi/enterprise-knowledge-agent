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

"""
bank = client.create_bank(
    bank_id="enterprise-knowledge",
    name="Enterprise Knowledge Agent"
)

print("Memory bank created!")


client.retain(
    bank_id="enterprise-knowledge",
    content="Sarah Chen is the project manager for Project Orion."
)

print("First memory stored!")
"""



"""
client.retain(
    bank_id="enterprise-knowledge",
    content=project_orion_data
)

print("Complete Project Orion data stored!")

"""

result = client.recall(
    bank_id="enterprise-knowledge",
    query= project_orion_data
)

print("Recall result:")
print(result)


