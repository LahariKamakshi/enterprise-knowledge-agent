
from groq import Groq
from hindsight_client import Hindsight
import json
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Groq connection
# -----------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# Hindsight connection
# -----------------------------

hindsight_client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)


# -----------------------------
# Sample email
# -----------------------------

email = """
Subject: Project Orion – Production Deployment Update

Hi Team,

Here is the latest update regarding Project Orion.

The production deployment is scheduled for Friday, October 2, 2026, at 10:00 PM IST.

David Miller will handle the database deployment, while Priya Rao will monitor the Azure SQL environment during the deployment. Lisa Johnson will perform the post-deployment QA testing.

The expected maintenance window is approximately 30 minutes. The team has also prepared a rollback procedure in case any critical issues occur during deployment.

Please complete your assigned tasks before Friday afternoon and report any blockers to Sarah Chen.

Regards,
Sarah Chen
Project Manager
Project Orion
"""


# -----------------------------
# Ask Groq to extract facts
# -----------------------------

prompt = f"""
You are an enterprise knowledge extraction system.

Extract useful factual information from this email.

Return ONLY valid JSON.
Do not use Markdown.
Do not add explanations.
Do not invent information.

Use exactly this structure:

{{
    "project": "",
    "people": [
        {{
            "name": "",
            "role": ""
        }}
    ],
    "tasks": [],
    "technologies": [],
    "deployment": {{
        "date": "",
        "time": ""
    }},
    "maintenance_window": "",
    "rollback_available": false,
    "deadlines": [],
    "instructions": []
}}

EMAIL:
{email}
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
# Convert LLM response to JSON
# -----------------------------

raw_response = response.choices[0].message.content

data = json.loads(raw_response)


print("\nLLM extraction successful! ✅")


# -----------------------------
# Convert JSON into memory
# -----------------------------

memory = f"""
Enterprise Project Memory

Project: {data['project']}

People and responsibilities:
"""

for person in data["people"]:
    memory += f"""
- {person['name']} is responsible for {person['role']}.
"""


memory += """

Tasks:
"""

for task in data["tasks"]:
    memory += f"""
- {task}
"""


memory += """

Technologies:
"""

for technology in data["technologies"]:
    memory += f"""
- {technology}
"""


memory += f"""

Deployment:
- Date: {data['deployment']['date']}
- Time: {data['deployment']['time']}

Maintenance window:
- {data['maintenance_window']}

Rollback available:
- {data['rollback_available']}

Deadlines:
"""

for deadline in data["deadlines"]:
    memory += f"""
- {deadline}
"""


memory += """

Instructions:
"""

for instruction in data["instructions"]:
    memory += f"""
- {instruction}
"""


# -----------------------------
# Display memory before storing
# -----------------------------

print("\nMemory prepared for Hindsight:")
print("--------------------------------")
print(memory)


# -----------------------------
# Store in Hindsight
# -----------------------------

hindsight_client.retain(
    bank_id="enterprise-knowledge",
    content=memory
)


print("\n✅ Enterprise knowledge stored in Hindsight!")