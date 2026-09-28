import os
import json
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from groq import Groq
from hindsight_client import Hindsight
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

BANK_ID = "enterprise-knowledge"

PROCESSED_EMAILS_FILE = "processed_emails.json"


# ============================================================
# GMAIL CONNECTION
# ============================================================

def connect_gmail():

    credentials = None

    # ========================================================
    # STEP 1: LOAD EXISTING TOKEN
    # ========================================================

    if os.path.exists("token.json"):

        print("Found existing Gmail token. 🔑")

        credentials = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # ========================================================
    # STEP 2: CHECK TOKEN
    # ========================================================

    if credentials and credentials.valid:

        print("Existing Gmail token is valid. ✅")

    # ========================================================
    # STEP 3: REFRESH EXPIRED TOKEN
    # ========================================================

    elif (
        credentials
        and credentials.expired
        and credentials.refresh_token
    ):

        print("Gmail token expired. Refreshing... 🔄")

        credentials.refresh(Request())

        with open("token.json", "w") as token:

            token.write(
                credentials.to_json()
            )

        print("Gmail token refreshed successfully. ✅")

    # ========================================================
    # STEP 4: FIRST-TIME AUTHENTICATION
    # ========================================================

    else:

        print("No valid Gmail token found.")
        print("Starting Google authentication...")

        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES
        )

        credentials = flow.run_local_server(
            port=0,
            access_type="offline",
            prompt="consent"
        )

        with open("token.json", "w") as token:

            token.write(
                credentials.to_json()
            )

        print("New Gmail token saved. ✅")

    # ========================================================
    # STEP 5: CONNECT TO GMAIL
    # ========================================================

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    print("Gmail connected successfully! ✅")

    return service


# ============================================================
# GROQ CONNECTION
# ============================================================

groq_client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# HINDSIGHT CONNECTION
# ============================================================

hindsight_client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)


# ============================================================
# AI EMAIL CLASSIFIER
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
{body[:1000]}
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
# EXTRACT EMAIL BODY
# ============================================================

def get_email_body(payload):

    body = ""

    if "parts" in payload:

        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                data = part["body"].get("data")

                if data:

                    body += base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

    else:

        data = payload.get("body", {}).get("data")

        if data:

            body = base64.urlsafe_b64decode(
                data
            ).decode(
                "utf-8",
                errors="ignore"
            )

    return body


# ============================================================
# EXTRACT ENTERPRISE FACTS USING GROQ
# ============================================================

def extract_facts(sender, subject, body):

    prompt = f"""
You are an enterprise knowledge extraction system.

Extract only useful long-term organizational knowledge
from the email below.

Return ONLY valid JSON.

Use these fields:

{{
    "project": "",
    "people": [],
    "tasks": [],
    "technologies": [],
    "decisions": [],
    "deadlines": [],
    "deployment": "",
    "issues": [],
    "instructions": []
}}

Rules:

- Do not invent information.
- Use empty strings or empty lists when information is missing.
- Keep names and responsibilities clear.
- Capture important project information.
- Capture technical information.
- Capture deadlines and deployment information.
- Capture business decisions.
- Capture important instructions.

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

    return response.choices[0].message.content


# ============================================================
# FORMAT EXTRACTED INFORMATION FOR HINDSIGHT
# ============================================================

def format_memory(sender, subject, facts):

    memory = f"""
Enterprise Email Memory

Sender:
{sender}

Subject:
{subject}

Extracted Knowledge:
{facts}
"""

    return memory


# ============================================================
# PROCESSED EMAIL TRACKING
# ============================================================

def load_processed_emails():

    if not os.path.exists(PROCESSED_EMAILS_FILE):

        return set()

    try:

        with open(
            PROCESSED_EMAILS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return set(data)

    except Exception:

        return set()


def save_processed_emails(processed_emails):

    with open(
        PROCESSED_EMAILS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            list(processed_emails),
            file,
            indent=2
        )


# ============================================================
# MAIN GMAIL INGESTION
# ============================================================

def ingest_emails():

    print("\n========================================")
    print(" Starting Gmail ingestion... 📧")
    print("========================================")

    service = connect_gmail()

    processed_emails = load_processed_emails()

    # Get the 10 most recent emails
    results = service.users().messages().list(
        userId="me",
        maxResults=10
    ).execute()

    messages = results.get("messages", [])

    print(f"Found {len(messages)} recent emails.")

    new_emails_processed = 0

    for index, message in enumerate(messages, start=1):

        message_id = message["id"]

        # ====================================================
        # SKIP ALREADY PROCESSED EMAILS
        # ====================================================

        if message_id in processed_emails:

            print("Email already processed. ⏭️")
            continue

        print("\n----------------------------------------")
        print(f"--- Email {index} ---")
        print("----------------------------------------")

        # ====================================================
        # GET FULL EMAIL
        # ====================================================

        email = service.users().messages().get(
            userId="me",
            id=message_id,
            format="full"
        ).execute()

        payload = email["payload"]

        # ====================================================
        # GET HEADERS
        # ====================================================

        headers = payload.get("headers", [])

        sender = ""
        subject = ""

        for header in headers:

            if header["name"].lower() == "from":

                sender = header["value"]

            elif header["name"].lower() == "subject":

                subject = header["value"]

        # ====================================================
        # GET BODY
        # ====================================================

        body = get_email_body(payload)

        print("From:", sender)
        print("Subject:", subject)

        # ====================================================
        # AI RELEVANCE CLASSIFICATION
        # ====================================================

        try:

            decision = classify_email(
                sender,
                subject,
                body
            )

        except Exception as e:

            print("Classifier error:", e)
            print("Email skipped.")

            continue

        if decision == "RELEVANT":

            print("Decision: ✅ RELEVANT")

        else:

            print("Decision: ❌ IRRELEVANT")

        # ====================================================
        # IGNORE IRRELEVANT EMAILS
        # ====================================================

        if decision == "IRRELEVANT":

            print("Email ignored.")

            processed_emails.add(message_id)

            save_processed_emails(
                processed_emails
            )

            continue

        # ====================================================
        # EXTRACT ENTERPRISE FACTS
        # ====================================================

        try:

            facts = extract_facts(
                sender,
                subject,
                body
            )

            print("LLM extraction: ✅")

        except Exception as e:

            print("LLM extraction failed:", e)

            continue

        # ====================================================
        # PREPARE HINDSIGHT MEMORY
        # ====================================================

        memory = format_memory(
            sender,
            subject,
            facts
        )

        # ====================================================
        # STORE IN HINDSIGHT
        # ====================================================

        try:

            hindsight_client.retain(
                bank_id=BANK_ID,
                content=memory
            )

            processed_emails.add(message_id)

            save_processed_emails(
                processed_emails
            )

            new_emails_processed += 1

            print("Hindsight storage: ✅")
            print("Email marked as processed. ✅")

        except Exception as e:

            print("Hindsight storage failed:", e)

    print("\n========================================")
    print(" Gmail ingestion completed! ✅")
    print(f" New emails processed: {new_emails_processed}")
    print("========================================")

    # IMPORTANT:
    # Do NOT close hindsight_client here.
    #
    # app.py will use this same module while running
    # the ingestion and then perform its own recall.
    #
    # Closing the client here could interfere with
    # the next Hindsight operation.

    return new_emails_processed


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    ingest_emails()