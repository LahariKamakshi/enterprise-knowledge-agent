from groq import Groq
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
# Ask LLM to extract facts
# -----------------------------

prompt = f"""
You are an enterprise knowledge extraction system.

Read the following email and extract only useful
enterprise information that should be remembered.

Focus on:
- Project names
- People and their roles
- Tasks and responsibilities
- Dates and deadlines
- Deployments
- Technologies
- Issues
- Decisions
- Important instructions

Do not invent information.

Return the result as simple bullet points.

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
# Display extracted facts
# -----------------------------

facts = response.choices[0].message.content

print("\nExtracted Enterprise Facts:")
print("--------------------------------")

print(facts)