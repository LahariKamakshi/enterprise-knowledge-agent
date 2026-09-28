from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# Groq connection
# -----------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# Sample enterprise email
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
# Extraction prompt
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


# -----------------------------
# Call Groq
# -----------------------------

response = client.chat.completions.create(
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
# Get LLM response
# -----------------------------

raw_response = response.choices[0].message.content


# -----------------------------
# Convert response to JSON
# -----------------------------

try:

    data = json.loads(raw_response)

    print("\nJSON extraction successful! ✅")
    print("--------------------------------")

    print(json.dumps(data, indent=4))


except json.JSONDecodeError:

    print("\nJSON extraction failed! ❌")
    print("--------------------------------")
    print(raw_response)