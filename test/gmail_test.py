from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from hindsight_client import Hindsight
import base64
import os
from dotenv import load_dotenv

load_dotenv()


# -----------------------------
# Gmail configuration
# -----------------------------

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


# -----------------------------
# Hindsight connection
# -----------------------------

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)


# -----------------------------
# Email relevance filter
# -----------------------------

def is_relevant_email(sender, subject, body):

    text = (sender + " " + subject + " " + body).lower()

    # Emails we don't want
    irrelevant_keywords = [
        "unsubscribe",
        "job alert",
        "jobrapido",
        "crunchyroll",
        "2-step verification",
        "security alert",
        "you allowed",
        "newsletter",
        "promotion",
        "promotional",
        "watch now",
        "opportunities near you"
    ]

    for keyword in irrelevant_keywords:
        if keyword in text:
            return False

    # Enterprise/work-related keywords
    relevant_keywords = [
        "project",
        "meeting",
        "task",
        "deadline",
        "client",
        "team",
        "manager",
        "deployment",
        "production",
        "database",
        "application",
        "software",
        "development",
        "bug",
        "issue",
        "release",
        "requirement",
        "architecture",
        "migration",
        "server",
        "azure",
        "aws",
        "jira",
        "sprint",
        "assigned",
        "milestone",
        "status update"
    ]

    for keyword in relevant_keywords:
        if keyword in text:
            return True

    return False


# -----------------------------
# Connect to Gmail
# -----------------------------

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    SCOPES
)

creds = flow.run_local_server(port=0)

service = build(
    "gmail",
    "v1",
    credentials=creds
)

print("Gmail connected successfully!")


# -----------------------------
# Get recent emails
# -----------------------------

results = service.users().messages().list(
    userId="me",
    maxResults=10
).execute()

messages = results.get("messages", [])


if not messages:

    print("No emails found.")

else:

    for i, msg in enumerate(messages, start=1):

        message_id = msg["id"]


        # -----------------------------
        # Get complete email
        # -----------------------------

        message = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()


        # -----------------------------
        # Extract sender and subject
        # -----------------------------

        headers = message["payload"]["headers"]

        sender = ""
        subject = ""

        for header in headers:

            if header["name"].lower() == "from":
                sender = header["value"]

            if header["name"].lower() == "subject":
                subject = header["value"]


        print(f"\n--- Email {i} ---")
        print("From:", sender)
        print("Subject:", subject)


        # -----------------------------
        # Extract email body
        # -----------------------------

        payload = message["payload"]

        body = ""


        if "parts" in payload:

            for part in payload["parts"]:

                if part["mimeType"] == "text/plain":

                    data = part["body"].get("data")

                    if data:

                        body = base64.urlsafe_b64decode(
                            data
                        ).decode("utf-8")

                    break


        elif payload["mimeType"] == "text/plain":

            data = payload["body"].get("data")

            if data:

                body = base64.urlsafe_b64decode(
                    data
                ).decode("utf-8")


        # -----------------------------
        # Check relevance
        # -----------------------------

        decision = is_relevant_email(
            sender,
            subject,
            body
        )


        if decision:

            print("Decision: ✅ RELEVANT")


            # -----------------------------
            # Prepare Hindsight memory
            # -----------------------------

            memory = f"""
Source: Gmail

From: {sender}
Subject: {subject}

Email content:
{body}
"""


            # -----------------------------
            # Store in Hindsight
            # -----------------------------

            client.retain(
                bank_id="enterprise-knowledge",
                content=memory
            )


            print("✅ Email stored in Hindsight!")


        else:

            print("Decision: ❌ IGNORED")


