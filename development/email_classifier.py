from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# GROQ CONNECTION
# ============================================================

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# EMAIL CLASSIFIER
# ============================================================

def classify_email(sender, subject, body):

    prompt = f"""
You are an enterprise email classification system.

Determine whether this email contains information
that could be useful as long-term organizational memory.

RELEVANT emails may contain:
- Projects
- Project updates
- Meetings
- Tasks
- Deadlines
- Team responsibilities
- Managers
- Clients
- Deployments
- Production changes
- Technical issues
- Bugs
- Requirements
- Architecture
- Databases
- Cloud infrastructure
- AWS or Azure
- Jira or sprint information
- Business decisions
- Important organizational instructions

IRRELEVANT emails include:
- Advertisements
- Newsletters
- Promotional campaigns
- Entertainment
- Shopping offers
- Generic job alerts
- Account/security notifications
- Personal emails with no enterprise relevance

Do not classify an email as relevant just because
it contains words such as "project", "software",
"development", or "team".

Look at the actual meaning of the email.

Return ONLY one word:

RELEVANT

or

IRRELEVANT

Sender:
{sender}

Subject:
{subject}

Email:
{body}
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


    decision = response.choices[0].message.content.strip().upper()


    if "RELEVANT" in decision and "IRRELEVANT" not in decision:
        return "RELEVANT"

    return "IRRELEVANT"


# ============================================================
# TEST EMAILS
# ============================================================

test_emails = [

    {
        "sender": "Canva World Tour",
        "subject": "Meet new learning buddies this Canva World Tour",
        "body": """
        Join the Canva World Tour and meet new learning buddies.
        Discover creative learning opportunities and events.
        """
    },

    {
        "sender": "Bavani",
        "subject": "Project Orion details",
        "body": """
        Project Orion production deployment is scheduled for
        October 2, 2026 at 10:00 PM IST.

        David Miller will handle database deployment.
        Priya Rao will monitor Azure SQL.
        Lisa Johnson will perform QA testing.
        """
    },

    {
        "sender": "Google",
        "subject": "Security alert",
        "body": """
        A security alert was detected on your Google account.
        """
    },

    {
        "sender": "Project Manager",
        "subject": "Production deployment update",
        "body": """
        The production deployment has been scheduled for Friday.
        Please complete your assigned tasks before the deadline.
        """
    }
]


# ============================================================
# TEST CLASSIFIER
# ============================================================

print("\n========================================")
print("       AI EMAIL CLASSIFIER")
print("========================================")


for i, email in enumerate(test_emails, start=1):

    decision = classify_email(
        email["sender"],
        email["subject"],
        email["body"]
    )


    print(f"\n--- Test Email {i} ---")
    print("From:", email["sender"])
    print("Subject:", email["subject"])
    print("Decision:", decision)


print("\n========================================")
print("Classifier testing completed! ✅")
print("========================================")
